import sys
import linuxcnc
import time
import os.path

def get_status_text(s):
    if 0 in s.homed[0:3]:
        return "NOT HOMED"
    elif s.task_state in [linuxcnc.STATE_ESTOP, linuxcnc.STATE_OFF]:
        return "POWER OFF"
    elif s.task_paused:
        return "PAUSED"
    elif s.task_mode != linuxcnc.MODE_AUTO:
        return "MANUAL CONTROL"
    else:
        return "RUNNING"

def get_linuxcnc_status():
    s = linuxcnc.stat()
    s.poll()
    
    status = "LinuxCNC status: %s\n" % get_status_text(s)
    status += "File: %s\n" % (os.path.basename(s.file)[:30])
    status += "X:        %7.2f mm\n" % (s.actual_position[0] - s.g5x_offset[0])
    status += "Y:        %7.2f mm\n" % (s.actual_position[1] - s.g5x_offset[1])
    status += "Z:        %7.2f mm\n" % (s.actual_position[2] - s.g5x_offset[2])
    status += "Velocity: %4.0f mm/min\n" % (s.current_vel * 60)
    status += "Spindle:  %4.0f RPM\n" % (s.spindle[0]['speed'] * s.spindle[0]['override'])
    
    return status

if __name__ == '__main__':
    print(get_linuxcnc_status())

