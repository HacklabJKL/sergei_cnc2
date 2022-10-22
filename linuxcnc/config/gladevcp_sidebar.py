import linuxcnc
from hal_glib import GStat
import time
GSTAT = GStat()

class SidebarHandler:
    def __init__(self, halcomp, builder, useropts):
        self.builder = builder
        self.command = linuxcnc.command()

        GSTAT.connect("user-system-changed", self.update_coordinate_selection)
        GSTAT.connect("all-homed", self.activate_default_g54)
        GSTAT.connect("all-homed", self.verify_g64)
        GSTAT.connect("state-on", self.verify_g64)

    def activate_default_g54(self, w):
        '''Make sure G54 coordinate system is active after start.'''
        time.sleep(0.1)
        self.command.mode(linuxcnc.MODE_MDI)
        self.command.mdi("G55")
        self.command.wait_complete()
        self.command.mdi("G54")
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

def get_handlers(halcomp,builder,useropts):
    return [SidebarHandler(halcomp,builder,useropts)]