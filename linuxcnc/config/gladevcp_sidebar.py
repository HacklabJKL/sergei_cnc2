#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import linuxcnc
import gtk
import glib
import hal
import hal_glib
import time
from hal_glib import GStat
import time
GSTAT = GStat()

class SidebarHandler:
    def __init__(self, halcomp, builder, useropts):
        self.halcomp = halcomp
        self.builder = builder
        self.command = linuxcnc.command()
        self.program_was_running = False
        self.paused_door_open = hal_glib.GPin(halcomp.newpin('paused_door_open', hal.HAL_BIT, hal.HAL_IN))
        self.stat = linuxcnc.stat()
        self.prev_status = None
        self.next_time = 0
        self.prev_offset = None
        self.prev_display_update = None
        self.last_home_time = time.time()

        self.builder.get_object('compon').set_active(True)
        self.builder.get_object('coolant_auto').set_active(True)

        GSTAT.connect("periodic", self.update_status)
        GSTAT.connect("user-system-changed", self.update_coordinate_selection)
        GSTAT.connect("all-homed", self.activate_default_g54)
        GSTAT.connect("all-homed", self.verify_g64)
        GSTAT.connect("state-on", self.verify_g64)
        GSTAT.connect("command-running", self.check_program_running)
        GSTAT.connect("command-stopped", self.check_program_stopped)

        self.set_status()

    def set_status(self, msg = None, warn = False, info = True):
        '''Set status indication text'''

        if msg == self.prev_status:
            return
        self.prev_status = msg

        # Gtk.Label does not have background, so set the background of the parent.
        lbl = self.builder.get_object('lblstatus')
        eb = self.builder.get_object('ebstatus')

        if not msg:
            lbl.set_text("")
            eb.modify_bg(gtk.STATE_NORMAL, None)
        elif warn:
            lbl.set_text("⚠\n" + msg)
            eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#ffffaa"))
        elif info:
            lbl.set_text(msg)
            eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#aaaaff"))
        else:
            lbl.set_text(msg)
            eb.modify_bg(gtk.STATE_NORMAL, None)

    def update_status(self, w):
        if time.time() < self.next_time:
            return

        try:
            self.stat.poll()
            self.next_time = time.time() + 0.2
        except:
            # Delay a bit if we lose connection for some reason
            self.set_status('?', False, False)
            self.stat = linuxcnc.stat()
            self.next_time = time.time() + 5.0
            return

        if hal.get_value("axisui.display-update-count") != self.prev_display_update:
            # Store offsets that were active when display was last updated
            self.prev_display_update = hal.get_value("axisui.display-update-count")
            self.prev_offset = self.get_offsets()

        if not (0 in self.stat.homed[:3]) and (time.time() - self.last_home_time) < 1:
            # Homing complete
            self.prev_offset = self.get_offsets()

        s = self.stat

        self.builder.get_object('compon').set_sensitive(not s.enabled)
        self.builder.get_object('compoff').set_sensitive(not s.enabled)

        if s.estop:
            self.set_status("Emergency stop active\nor power off")
        elif hal.get_value("powerctl.power_enable") and not hal.get_value("powerctl.power_good"):
            self.set_status("+48V power is off\nPossible fuse trip?\nTurn off and on to reset", True)
        elif not s.enabled and hal.get_value("halui.machine.on"):
            self.set_status("Software stop\nRe-enable power on toolbar", True)
        elif not hal.get_value("powerctl.power_enable_raw"):
            self.set_status("Power disabled due to fault\nRe-enable power on toolbar", True)
        elif (0 in s.homed[:3]):
            if not s.inpos:
                self.last_home_time = time.time()
                self.set_status("Homing in progress")
            elif (time.time() - self.last_home_time) < 1:
                self.set_status("Homing in progress")
            elif hal.get_value("powerctl.allow_auto"):
                self.set_status("Press \"Home all\"\nto initialize machine")
            else:
                self.set_status("Close door and\npress \"Home all\"\nto initialize machine")
        elif s.feedrate <= 0.01:
            self.set_status("Feedrate override is set to 0\nMovements paused", True)
        elif s.rapidrate <= 0.01:
            self.set_status("Rapid override is set to 0\nMovements paused", True)
        elif s.spindle[0]['override'] <= 0.01:
            self.set_status("Spindle override is set to 0\nMovements paused", True)
        elif self.paused_door_open.get():
            self.set_status("Close door or hold down RUN\nto enable automatic moves", True)
        elif hal.get_value("powerctl.spindle_on") and hal.get_value("powerctl.probe_connected"):
            self.set_status("Cannot start spindle\nwhen probe connected!", True)
        elif hal.get_value("powerctl.spindle_on") and not hal.get_value("powerctl.spindle_enable"):
            self.set_status("Close door to start spindle", True)
        elif hal.get_value("powerctl.spindle_enable") and not hal.get_value("powerctl.spindle_at_speed_filtered"):
            self.set_status("Waiting for spindle to start")
        elif abs(hal.get_value("motordrive.2.offset") - hal.get_value("motordrive.2.offset-req")) > 0.1:
            if abs(hal.get_value("motordrive.2.offset") - hal.get_value("motordrive.2.max-offset")) < 0.1:
                self.set_status("Z offset is active,\nlimited by max Z:\n(%+0.2f mm)"
                    % hal.get_value("motordrive.2.offset"), True)
            elif hal.get_value("powerctl.allow_auto"):
                self.set_status("Z offset movement in progress:\n(%+0.2f mm)\n(open door to pause)"
                    % hal.get_value("motordrive.2.offset"), True)
            else:
                self.set_status("Z offset movement paused\n(%+0.0f mm)\n(close door to continue)"
                    % hal.get_value("motordrive.2.offset"), True)
        elif self.stat.file and self.get_offsets() != self.prev_offset and self.stat.task_mode != linuxcnc.MODE_AUTO:
            self.set_status("Coordinate system\nchanged, press\nreload to update preview.")
        elif abs(hal.get_value("motordrive.2.offset")) > 0.01:
            self.set_status("Z offset is active:\n(%+0.2f mm)"
                % hal.get_value("motordrive.2.offset"), True)
        else:
            self.set_status()

    def get_offsets(self):
        return (self.stat.g5x_offset, self.stat.g92_offset, self.stat.rotation_xy)

    def activate_default_g54(self, w):
        '''Make sure G54 coordinate system is active after start.'''
        time.sleep(0.1)
        self.command.mode(linuxcnc.MODE_MDI)
        self.command.mdi("G55")
        self.command.wait_complete()
        self.command.mdi("G54")
        self.command.wait_complete()
        self.command.mdi("M52")
        self.command.wait_complete()

    def update_coordinate_selection(self, w, data):
        '''Update the state of coordinate selection buttons in sidebar'''
        system = int(data)
        self.builder.get_object('selectg54').set_active(system == 1)
        self.builder.get_object('selectg55').set_active(system == 2)
        self.builder.get_object('selectg56').set_active(system == 3)
        self.builder.get_object('selectg57').set_active(system == 4)

        other_sys = (system not in [1, 2, 3, 4])
        self.builder.get_object('selectg54').set_inconsistent(other_sys)
        self.builder.get_object('selectg55').set_inconsistent(other_sys)
        self.builder.get_object('selectg56').set_inconsistent(other_sys)
        self.builder.get_object('selectg57').set_inconsistent(other_sys)

    def verify_g64(self, w, data = None):
        '''If G64 (interpolation) is active, verify sane tolerances.
        This is to workaround LinuxCNC issue: https://github.com/LinuxCNC/linuxcnc/issues/177
        '''

        time.sleep(0.05)
        s = linuxcnc.stat()
        s.poll()

        all_homed = (0 not in s.homed[:3])
        g64_active = (640 in s.gcodes)
        if all_homed and g64_active:
            self.command.mode(linuxcnc.MODE_MDI)
            self.command.mdi("G64 P0.01 Q0.01")

    def check_program_running(self, w, data = None):
        self.program_was_running = GSTAT.is_auto_running()

    def check_program_stopped(self, w, data = None):
        '''When program is aborted, make sure M2 gets run to restore any modal settings.'''
        if self.program_was_running:
            time.sleep(0.1)
            self.command.mode(linuxcnc.MODE_MDI)
            self.command.wait_complete()
            self.command.mdi("M2")
            self.program_was_running = False

def get_handlers(halcomp,builder,useropts):
    return [SidebarHandler(halcomp,builder,useropts)]
