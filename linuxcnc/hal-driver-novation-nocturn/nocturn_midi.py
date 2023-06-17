#!/usr/bin/env python2

'''Driver for Novation Nocturn USB controller using rtmidi interface.

Mapping information from https://github.com/dewert/nocturn-linux-midi

Note that this uses the Python2 module rtmidi from
https://github.com/patrickkidd/pyrtmidi/
not the newer python3-rtmidi.
'''

import time
import rtmidi
from collections import namedtuple

class NocturnMidi:
    buttonaddrs =  [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]
    encoderaddrs = [64, 65, 66, 67, 74, 68, 69, 70, 71]
    encoderleds =  [64, 65, 66, 67, 80, 68, 69, 70, 71]
    encodermodes = [72, 73, 74, 75, 81, 76, 77, 78, 79]
    encodertouch = [96, 97, 98, 99, 82, 100, 101, 102, 103]
    encoderpress = [0, 0, 0, 0, 81, 0, 0, 0, 0]
    slideraddrs = [72]
    slidertouch = [83]

    def __init__(self):
        self.encsums = [0] * len(self.encoderaddrs)
        self.encprevdir = [0] * len(self.encoderaddrs)
        self.midi_in = rtmidi.RtMidiIn()
        self.midi_out = rtmidi.RtMidiOut()
        self.midi_port_idx = None
        self.midi_port_count = 0
        self.check_midi_connection()
    
    def __iter__(self):
        while True:
            v = self.parse_inputs()
            if v:
                yield v
            else:
                self.check_midi_connection()
                time.sleep(0.05)

    def check_midi_connection(self):
        '''(Re)open midi port, required after USB disconnection'''
        new_midi_port_count = self.midi_in.getPortCount()

        if new_midi_port_count == self.midi_port_count:
            return
        
        self.midi_port_count = new_midi_port_count
        print("Detected MIDI port change, %d ports available" % self.midi_port_count)

        new_port_idx = None
        for i in range(self.midi_port_count):
            if 'Nocturn' in self.midi_in.getPortName(i):
                new_port_idx = i

        if new_port_idx != self.midi_port_idx:
            self.midi_port_idx = new_port_idx
            self.midi_in.closePort()
            self.midi_out.closePort()
            self.midi_in = rtmidi.RtMidiIn()
            self.midi_out = rtmidi.RtMidiOut()
            if self.midi_port_idx is not None:
                time.sleep(0.5)
                print("Connecting Novation Nocturn on port ", self.midi_port_idx)
                self.midi_in.openPort(self.midi_port_idx)
                self.midi_out.openPort(self.midi_port_idx)

                for i in range(len(self.buttonaddrs)):
                    self.set_button_led(i, False)
                    time.sleep(0.01)
                
                for i in range(len(self.encoderleds)):
                    self.set_encoder_leds(i, 0, 0)
                    time.sleep(0.01)
                

    def parse_inputs(self):
        '''Parse midi messages from the controller and return a tuple:
        ('btn09', True) <-- Button 9 down
        ('btn09', False) <-- Button 9 up
        ('enc02', -1) <-- Encoder 2 counter-clockwise rotation
        ('enc02_touch', True) <-- Encoder 2 touched
        ('slider00_pos', 0.8) <-- Slider position changed
        ('overflow', 0) <-- Some events have been lost

        Returns None if no new messages
        '''
        msg = self.midi_in.getMessage()
        if not msg:
            return None

        addr = msg.getControllerNumber()
        value = msg.getControllerValue()
        timestamp = msg.getTimeStamp()
        # print(addr, value, timestamp)
        if addr in self.buttonaddrs:
            idx = self.buttonaddrs.index(addr)
            return ('btn%02d' % idx, value != 0)
        
        elif addr in self.encoderaddrs:
            idx = self.encoderaddrs.index(addr)
            if value < 64:
                self.encsums[idx] += value
            else:
                self.encsums[idx] -= 128 - value
            
            # We get two events per one encoder detent, use it for filtering.
            # Additionally filter out glitches were direction reverses for a short
            # time due to the way the hardware reads the encoders.
            if timestamp > 0.5:
                self.encsums[idx] = 0
            
            delta = int(self.encsums[idx] / 3.0)

            reversal = ((delta > 0 and self.encprevdir[idx] < 0) or
                        (delta < 0 and self.encprevdir[idx] > 0))
            if reversal and timestamp < 0.1 and abs(self.encsums[idx]) < 5:
                delta = 0

            self.encsums[idx] -= delta * 2
            if delta != 0:
                self.encprevdir[idx] = delta
                return ('enc%02d' % idx, delta)
            else:
                return self.parse_inputs()

        elif addr in self.encodertouch:
            idx = self.encodertouch.index(addr)
            self.encsums[idx] = 0
            return ('enc%02d_touch' % idx, value != 0)

        elif addr in self.encoderpress:
            idx = self.encoderpress.index(addr)
            self.encsums[idx] = 0
            return ('enc%02d_press' % idx, value != 0)

        elif addr in self.slideraddrs:
            idx = self.slideraddrs.index(addr)
            return ('slider%02d' % idx, value / 127.0)
        
        elif addr in self.slidertouch:
            idx = self.slidertouch.index(addr)
            return ('slider%02d_touch' % idx, value != 0)

        elif addr == 73:
            # Seems to be related to the slider
            return ('unknown', value)
        
        else:
            print("NocturnMidi: Unknown message: ", addr, value)
            return ('unknown', value)
        
        return None
    
    def set_encoder_leds(self, index, mode, value):
        '''Set LED ring around encoder.
        Modes:
            0: start from left,
            1: start from right,
            2: start from center, one way,
            3: start from center, two ways,
            4: single led,
            5: single led, inverted
        '''
        if self.midi_out.isPortOpen():
            value = min(127, max(0, int(value * 127)))
            self.midi_out.sendMessage(rtmidi.MidiMessage.controllerEvent(1,
                self.encodermodes[index], 16 * mode))
            self.midi_out.sendMessage(rtmidi.MidiMessage.controllerEvent(1,
                self.encoderleds[index], value))
    
    def set_button_led(self, index, enabled):
        if self.midi_out.isPortOpen():
            self.midi_out.sendMessage(rtmidi.MidiMessage.controllerEvent(1,
                self.buttonaddrs[index], int(enabled)))
            time.sleep(0.01)

    def leds_off(self):
        for i in range(len(self.buttonaddrs)):
            self.set_button_led(i, False)
        
        for i in range(len(self.encoderleds)):
            self.set_encoder_leds(i, 0, 0)

if __name__ == '__main__':
    try:
        nocturn = NocturnMidi()
        for key, val in nocturn:
            print(key, val)
    except KeyboardInterrupt:
        raise SystemExit
