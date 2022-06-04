#!/usr/bin/env python2

'''Using Novation Nocturn as LinuxCNC jog controller.

The hardware communication side is in nocturn_midi.py.
This file implements the controller logic and ties to LinuxCNC HAL.

Instead of exposing a set of pins and connecting them, this
script takes the lazy approach and just uses setp to write
e.g. halui.axis.x.increment-plus directly.
'''

import hal
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
            step, speed = 10, 1000
        elif pos == 1:
            step, speed = 1, 1000
        elif pos == 2:
            step, speed = 0.1, 100
        elif pos == 3:
            step, speed = 0.01, 100
        
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

class Button:
    '''Button press to HAL pin'''
    def __init__(self, comp, pinname):
        self.comp = comp
        self.pinname = pinname
        self.comp.newpin(self.pinname, hal.HAL_BIT, hal.HAL_OUT)
    
    def __call__(self, event):
        self.comp[self.pinname] = event[1]

class Led:
    '''Polling to LED state'''
    def __init__(self, comp, hw, pinname, led_idx, blink_time = 0.0, invert = False):
        self.comp = comp
        self.hw = hw
        self.pinname = pinname
        self.led_idx = led_idx
        self.blink_time = blink_time
        self.invert = invert
        self.comp.newpin(self.pinname, hal.HAL_BIT, hal.HAL_IN)
    
    def __call__(self, event):
        if self.comp[self.pinname] ^ self.invert:
            if self.blink_time > 0:
                state = ((time.time() % self.blink_time) < (self.blink_time / 2.0))
            else:
                state = True
        else:
            state = False
        
        self.hw.set_button_led(self.led_idx, state)

class NocturnController:
    def __init__(self):
        self.comp = hal.component("nocturn")
        self.hw = nocturn_midi.NocturnMidi()
        self.handlers = {
            'slider00': JogSpeed(self.comp),
            'enc00': JogMotion(self.comp, 'x'),
            'enc01': JogMotion(self.comp, 'y'),
            'enc02': JogMotion(self.comp, 'z'),
            'btn15': Button(self.comp, "home_all"),
            'poll': [
                Led(self.comp, self.hw, 'machine_homed', 15, blink_time = 1.0, invert = True)
            ]
        }
        
        self.comp.ready()

    def poll(self):
        event = self.hw.parse_inputs()
        if event:
            self.handle_event(event)
        else:
            self.handle_event(('poll', None))
            self.hw.check_midi_connection()
            time.sleep(0.05)

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
