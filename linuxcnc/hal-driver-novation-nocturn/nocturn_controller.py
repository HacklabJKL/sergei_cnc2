#!/usr/bin/env python2

'''Using Novation Nocturn as LinuxCNC jog controller.

The hardware communication side is in nocturn_midi.py.
This file implements the controller logic and ties to LinuxCNC HAL.

Instead of exposing a set of pins and connecting them, this
script takes the lazy approach and just uses setp to write
e.g. halui.axis.x.increment-plus directly.
'''

import hal
import linuxcnc
import time
import nocturn_midi

def delay():
    '''Delay to let LinuxCNC GUI notice action'''
    time.sleep(0.05)

class JogSpeed:
    '''Control jog speed and increment based on slider position'''
    increment = 'jog_increment'
    speed = 'jog_speed'
        
    def __init__(self, comp):
        self.comp = comp
        self.comp.newpin(self.increment, hal.HAL_FLOAT, hal.HAL_OUT)
        self.comp.newpin(self.speed, hal.HAL_FLOAT, hal.HAL_OUT)
    
    def __call__(self, event):
        pos = round(event[1] * 3)
        if pos == 0:
            step, speed = 10, 2000
        elif pos == 1:
            step, speed = 1, 1000
        elif pos == 2:
            step, speed = 0.1, 100
        elif pos == 3:
            step, speed = 0.01, 10
        
        self.comp[self.increment] = step
        self.comp[self.speed] = speed

class JogMotion:
    '''Jog single axis with an encoder'''

    def __init__(self, comp, axis):
        self.comp = comp
        self.counts = "jog_%s_counts" % axis
        self.comp.newpin(self.counts, hal.HAL_S32, hal.HAL_OUT)

    def __call__(self, event):
        self.comp[self.counts] += event[1]

class AutoZeroEncoder:
    '''Encoder that resets value when machine is powered off'''
    def __init__(self, comp, pinname):
        self.comp = comp
        self.pinname = pinname
        self.comp.newpin(self.pinname, hal.HAL_S32, hal.HAL_OUT)

        try:
            self.comp.newpin('machine-is-on', hal.HAL_BIT, hal.HAL_IN)
        except ValueError:
            pass
    
    def __call__(self, event):
        if self.comp['machine-is-on'] == 0:
            self.comp[self.pinname] = 0
        elif event[0] != 'poll':
            self.comp[self.pinname] += event[1]

class Button:
    '''Button press to HAL pin'''
    def __init__(self, comp, pinname):
        self.comp = comp
        self.pinname = pinname
        self.comp.newpin(self.pinname, hal.HAL_BIT, hal.HAL_OUT)
    
    def __call__(self, event):
        self.comp[self.pinname] = event[1]

class ToggleButton:
    '''Toggle HAL pin on every press'''
    def __init__(self, comp, pinname, default = False):
        self.comp = comp
        self.pinname = pinname
        self.comp.newpin(self.pinname, hal.HAL_BIT, hal.HAL_OUT)
        self.comp[self.pinname] = default
    
    def __call__(self, event):
        if event[1]:
            self.comp[self.pinname] = not self.comp[self.pinname]

class MDIButton:
    '''Button that runs MDI command'''
    def __init__(self, mdi_command):
        self.mdi_command = mdi_command
    
    def __call__(self, event):
        if event[1]:
            cmd = linuxcnc.command()
            cmd.mode(linuxcnc.MODE_MDI)
            cmd.wait_complete()
            cmd.mdi(self.mdi_command)

class Pulse:
    '''Give pulse on a pin'''
    def __init__(self, comp, pinname):
        self.comp = comp
        self.pinname = pinname
        try:
            self.comp.newpin(self.pinname, hal.HAL_BIT, hal.HAL_OUT)
        except ValueError:
            pass # Duplicate pin
    
    def __call__(self, event):
        if event[0] == 'poll':
            self.comp[self.pinname] = 0
        else:
            self.comp[self.pinname] = 1

class Led:
    '''Polling HAL pin to LED state'''
    def __init__(self, comp, hw, pinname, led_idx, blink_time = 0.0, invert = False):
        self.comp = comp
        self.hw = hw
        self.pinname = pinname
        self.led_idx = led_idx
        self.blink_time = blink_time
        self.invert = invert
        self.prev_state = None
        try:
            self.comp.newpin(self.pinname, hal.HAL_BIT, hal.HAL_IN)
        except ValueError:
            pass # Duplicate pin
    
    def __call__(self, event):
        if self.comp[self.pinname] ^ self.invert:
            if self.blink_time > 0:
                state = ((time.time() % self.blink_time) < (self.blink_time / 2.0))
            else:
                state = True
        else:
            state = False
        
        if self.hw.midi_port_idx is None:
            self.prev_state = None
        elif state != self.prev_state:
            self.prev_state = state
            self.hw.set_button_led(self.led_idx, state)

class RelativeZeroLed:
    '''Light led if relative coordinate is zero'''
    def __init__(self, comp, hw, pinname, led_idx):
        self.comp = comp
        self.hw = hw
        self.pinname = pinname
        self.led_idx = led_idx
        self.prev_state = None
        self.comp.newpin(self.pinname, hal.HAL_FLOAT, hal.HAL_IN)
    
    def __call__(self, event):
        state = abs(self.comp[self.pinname]) < 0.01

        if self.hw.midi_port_idx is None:
            self.prev_state = None
        elif state != self.prev_state:
            self.prev_state = state
            self.hw.set_button_led(self.led_idx, state)
        

class EncoderRing:
    '''Show current value on encoder led ring as a filled scale'''
    def __init__(self, comp, hw, pinname, enc_idx, minval = 0.0, maxval = 1.0, ledmode = 2, wrap = False):
        self.comp = comp
        self.hw = hw
        self.pinname = pinname
        self.enc_idx = enc_idx
        self.minval = minval
        self.maxval = maxval
        self.ledmode = ledmode
        self.wrap = wrap
        self.comp.newpin(self.pinname, hal.HAL_FLOAT, hal.HAL_IN)
    
    def __call__(self, event):
        v = (self.comp[self.pinname] - self.minval) / (self.maxval - self.minval)
        if self.wrap: v = v % 1.0
        self.hw.set_encoder_leds(self.enc_idx, self.ledmode, v)

class NocturnController:
    def __init__(self):
        self.comp = hal.component("nocturn")
        self.hw = nocturn_midi.NocturnMidi()
        self.handlers = {
            'slider00': JogSpeed(self.comp),
            'enc08': AutoZeroEncoder(self.comp, 'x_offset'),
            'enc07': AutoZeroEncoder(self.comp, 'y_offset'),
            'enc06': AutoZeroEncoder(self.comp, 'z_offset'),
            'enc05': AutoZeroEncoder(self.comp, 'spindle_override'),
            'enc04': AutoZeroEncoder(self.comp, 'feed_override'),
            'enc03': [JogMotion(self.comp, 'x'),     Pulse(self.comp, "start_jog")],
            'enc02': [JogMotion(self.comp, 'y'),     Pulse(self.comp, "start_jog")],
            'enc01': [JogMotion(self.comp, 'z'),     Pulse(self.comp, "start_jog")],
            'enc00': [JogMotion(self.comp, 'a'),     Pulse(self.comp, "start_jog")],
            'btn03': [Button(self.comp, "x_minus"),  Pulse(self.comp, "start_jog")],
            'btn11': [Button(self.comp, "x_plus"),   Pulse(self.comp, "start_jog")],
            'btn02': [Button(self.comp, "y_minus"),  Pulse(self.comp, "start_jog")],
            'btn10': [Button(self.comp, "y_plus"),   Pulse(self.comp, "start_jog")],
            'btn01': [Button(self.comp, "z_minus"),  Pulse(self.comp, "start_jog")],
            'btn09': [Button(self.comp, "z_plus"),   Pulse(self.comp, "start_jog")],
            'btn00': [Button(self.comp, "a_minus"),  Pulse(self.comp, "start_jog")],
            'btn08': [Button(self.comp, "a_plus"),   Pulse(self.comp, "start_jog")],
            'btn07': ToggleButton(self.comp, "clear_offsets", default = True),
            'btn06': ToggleButton(self.comp, "lift_z"),
            'btn15': MDIButton('G10 L20 P0 X0'),
            'btn14': MDIButton('G10 L20 P0 Y0'),
            'btn13': MDIButton('G10 L20 P0 Z0'),
            'btn12': MDIButton('o<z_probe_pad> call'),
            'btn05': MDIButton('o<tool_change_pos> call'),
            'btn04': MDIButton('o<tool_length_probe> call'),
            'poll': [
                Pulse(self.comp, "start_jog"),
                Led(self.comp, self.hw, 'jog_enabled', 0),
                Led(self.comp, self.hw, 'jog_enabled', 1),
                Led(self.comp, self.hw, 'jog_enabled', 2),
                Led(self.comp, self.hw, 'jog_enabled', 3),
                Led(self.comp, self.hw, 'jog_enabled', 8),
                Led(self.comp, self.hw, 'jog_enabled', 9),
                Led(self.comp, self.hw, 'jog_enabled', 10),
                Led(self.comp, self.hw, 'jog_enabled', 11),
                Led(self.comp, self.hw, 'clear_offsets', 7, invert = True),
                Led(self.comp, self.hw, 'lift_z', 6),
                EncoderRing(self.comp, self.hw, 'led_x_offset', 8, 0.0, 1.0, 4, True),
                EncoderRing(self.comp, self.hw, 'led_y_offset', 7, 0.0, 1.0, 4, True),
                EncoderRing(self.comp, self.hw, 'led_z_offset', 6, 0.0, 1.0, 4, True),
                EncoderRing(self.comp, self.hw, 'led_spindle_override', 5, 0.0, 2.0, 0),
                EncoderRing(self.comp, self.hw, 'led_feed_override', 4, 0.0, 2.0, 0),
                RelativeZeroLed(self.comp, self.hw, 'rel_x', 15),
                RelativeZeroLed(self.comp, self.hw, 'rel_y', 14),
                RelativeZeroLed(self.comp, self.hw, 'rel_z', 13),
            ]
        }

        self.handlers['poll'] += [
            self.handlers['enc08'],
            self.handlers['enc07'],
            self.handlers['enc06'],
            self.handlers['enc05'],
            self.handlers['enc04'],
        ]
        
        self.comp.ready()

    def poll(self):
        event = self.hw.parse_inputs()
        if event:
            self.handle_event(event)
        else:
            time.sleep(0.05)
            self.handle_event(('poll', None))
            self.hw.check_midi_connection()

    def handle_event(self, event):
        if event[0] in self.handlers:
            handlers = self.handlers[event[0]]
            
            try:
                for handler in handlers:
                    handler(event)
            except TypeError:
                handlers(event)
    
if __name__ == '__main__':
    try:
        nocturn = NocturnController()
        while True:
            nocturn.poll()
    except KeyboardInterrupt:
        raise SystemExit
