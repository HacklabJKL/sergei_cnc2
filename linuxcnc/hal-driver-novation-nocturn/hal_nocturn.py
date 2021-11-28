#!/usr/bin/env python

'''This is a LinuxCNC userspace HAL driver for Novation Nocturn USB controller.
It allows to use it for e.g. jog control & generic buttons.

Mapping information from https://github.com/dewert/nocturn-linux-midi

Note that this uses the Python2 module rtmidi from
https://github.com/patrickkidd/pyrtmidi/
not the newer python3-rtmidi.
'''

import hal
import time
import rtmidi
import sys
import binascii

class NocturnHAL:
    buttonaddrs = [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]
    encoderaddrs = [64, 65, 66, 67, 74, 68, 69, 70, 71]
    encoderleds = [64, 65, 66, 67, 80, 68, 69, 70, 71]
    encodertouch = [96, 97, 98, 99, 82, 100, 101, 102, 103]
    encoderpress = [0, 0, 0, 0, 81, 0, 0, 0, 0]
    slideraddrs = [72]
    slidertouch = [83]

    def __init__(self):
        self.open_midi()
        self.c = hal.component("nocturn")
        
        self.prev_button_leds = [None] * len(self.buttonaddrs)
        self.prev_encoder_leds = [None] * len(self.encoderleds)
        
        for i in range(len(self.buttonaddrs)):
            self.c.newpin("btn%02d" % i, hal.HAL_BIT, hal.HAL_OUT)
            self.c.newpin("btn%02d_led" % i, hal.HAL_BIT, hal.HAL_IN)
        
        for i in range(len(self.encoderaddrs)):
            self.c.newpin("enc%02d_up" % i, hal.HAL_BIT, hal.HAL_OUT)
            self.c.newpin("enc%02d_dn" % i, hal.HAL_BIT, hal.HAL_OUT)
            self.c.newpin("enc%02d_touch" % i, hal.HAL_BIT, hal.HAL_OUT)
            self.c.newpin("enc%02d_pos" % i, hal.HAL_S32, hal.HAL_OUT)
            self.c.newpin("enc%02d_led" % i, hal.HAL_FLOAT, hal.HAL_IN)
            
            if self.encoderpress[i] != 0:
                self.c.newpin("enc%02d_press" % i, hal.HAL_BIT, hal.HAL_OUT)
        
        for i in range(len(self.slideraddrs)):
            self.c.newpin("slider%02d_pos" % i, hal.HAL_FLOAT, hal.HAL_OUT)
            self.c.newpin("slider%02d_touch" % i, hal.HAL_BIT, hal.HAL_OUT)

        self.c.ready()

    def open_midi(self):
        self.midi_in = rtmidi.RtMidiIn()
        for i in range(self.midi_in.getPortCount()):
            if 'Nocturn' in self.midi_in.getPortName(i):
                self.midi_in.openPort(i)
                break
        else:
            print("Couldn't find Nocturn MIDI input")
        
        self.midi_out = rtmidi.RtMidiOut()
        for i in range(self.midi_out.getPortCount()):
            if 'Nocturn' in self.midi_out.getPortName(i):
                self.midi_out.openPort(i)
                break
        else:
            print("Couldn't find Nocturn MIDI output")

    def parse_inputs(self):
        msg = self.midi_in.getMessage()
        if msg:
            addr = msg.getControllerNumber()
            value = msg.getControllerValue()
            timestamp = msg.getTimeStamp()
            #print(addr, value, timestamp)
            if addr in self.buttonaddrs:
                idx = self.buttonaddrs.index(addr)
                if value == 0:
                    self.c['btn%02d' % idx] = 0
                else:
                    self.c['btn%02d' % idx] = 1
            
            elif addr in self.encoderaddrs:
                idx = self.encoderaddrs.index(addr)
                if value == 1:
                    self.c['enc%02d_up' % idx] = 1
                    self.c['enc%02d_pos' % idx] += 1
                    time.sleep(0.003)
                    self.c['enc%02d_up' % idx] = 0
                    time.sleep(0.003)
                elif value == 127:
                    self.c['enc%02d_dn' % idx] = 1
                    self.c['enc%02d_pos' % idx] -= 1
                    time.sleep(0.003)
                    self.c['enc%02d_dn' % idx] = 0
                    time.sleep(0.003)

            elif addr in self.encodertouch:
                idx = self.encodertouch.index(addr)
                if value == 0:
                    self.c['enc%02d_touch' % idx] = 0
                else:
                    self.c['enc%02d_touch' % idx] = 1

            elif addr in self.encoderpress:
                idx = self.encoderpress.index(addr)
                if value == 0:
                    self.c['enc%02d_press' % idx] = 0
                else:
                    self.c['enc%02d_press' % idx] = 1

            elif addr in self.slideraddrs:
                idx = self.slideraddrs.index(addr)
                self.c['slider%02d_pos' % idx] = value / 127.0
            
            elif addr in self.slidertouch:
                idx = self.slidertouch.index(addr)
                if value == 0:
                    self.c['slider%02d_touch' % idx] = 0
                else:
                    self.c['slider%02d_touch' % idx] = 1

            elif addr == 73:
                # I don't know what is happening with message 73, but it seems
                # to sometimes replace the button/touch release messages.
                for i in range(len(self.encoderaddrs)):
                    if self.encoderpress[i]:
                        self.c['enc%02d_press' % i] = 0
                for i in range(len(self.buttonaddrs)):
                    self.c['btn%02d' % i] = 0

            return True
        else:
            return False

    def update_leds(self):
        button_leds = [self.c["btn%02d_led" % i] for i in range(len(self.buttonaddrs))]
        encoder_leds = [self.c["enc%02d_led" % i] for i in range(len(self.encoderleds))]
        
        for i, addr in enumerate(self.buttonaddrs):
            if button_leds[i] != self.prev_button_leds[i]:
                self.midi_out.sendMessage(rtmidi.MidiMessage.controllerEvent(1, addr, button_leds[i]))
        
        for i, addr in enumerate(self.encoderleds):
            if encoder_leds[i] != self.prev_encoder_leds[i]:
                val = int(round(encoder_leds[i] * 127))
                if val < 0: val = 0
                if val > 127: val = 127
                self.midi_out.sendMessage(rtmidi.MidiMessage.controllerEvent(1, addr, val))

        self.prev_button_leds = button_leds
        self.prev_encoder_leds = encoder_leds

if __name__ == '__main__':
    try:
        nocturn = NocturnHAL()
        last_ok = time.time()
        while True:
            while nocturn.parse_inputs():
                last_ok = time.time()
            nocturn.update_leds()
            time.sleep(0.01)
            
            if time.time() - last_ok > 30:
                last_ok = time.time()
                nocturn.open_midi()
    except KeyboardInterrupt:
        raise SystemExit
