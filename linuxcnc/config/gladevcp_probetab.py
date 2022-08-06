# Simple probe tab for use with LinuxCNC & gladevcp
# Inspired by & reused icons from probe screen by Serguei Glavatski / vers.by
# Copyright 2022 Petteri Aimonen
# License GNU GPL 2 or later.

import linuxcnc
import math
import os
import datetime
import glib

class ProbeOperation:
    '''Basic probe operation, probe in linear move and return to original position.'''

    def __init__(self, parent, resultname, probe_deltas):
        self.parent = parent
        self.resultname = resultname
        self.probe_deltas = probe_deltas
        self.stat = self.parent.stat
        self.command = self.parent.command
        self.prev_command_serial = None
        self.step = 0
        self.status = ''
        self.result = None
        self.error = None
    
    def __str__(self):
        if self.error:
            return self.error
        elif self.result:
            return "Probe " + self.resultname + " done"
        elif self.stat.paused:
            return self.status + " (paused)"
        else:
            return self.status

    def fraction(self):
        return self.step / 4.0

    def done(self):
        return self.error or self.result

    def poll(self):
        '''Check current operation status and execute next steps.
        If complete, returns True.
        '''

        if self.done():
            return True # All done

        status = self.command.wait_complete(0.1)
        if status < 0:
            # Command still running
            return False
        
        if status == linuxcnc.RCS_ERROR:
            self.error = "Command failed"
            return

        self.stat.poll()
        if self.stat.paused:
            return

        if self.stat.probing:
            return

        if self.step == 0:
            # First step: go to MDI mode
            self.status = 'Enter MDI mode'
            self.command.mode(linuxcnc.MODE_MDI)
            self.step = 1
        
        elif self.step == 1:
            # Start probing towards workpiece, stop on contact
            if self.stat.probe_val:
                self.error = self.resultname + ": Probe already tripped at start!"
                return

            self.status = self.resultname + ': Probe towards surface'
            self.original_pos = self.stat.position
            self.original_g91 = 910 in self.stat.gcodes
            self.command.mdi("G91 G38.3 X%0.3f Y%0.3f Z%0.3f F%0.3f" %
                (self.probe_deltas[0], self.probe_deltas[1], self.probe_deltas[2], self.parent.search_speed))
            self.step = 2
        
        elif self.step == 2:
            if not self.stat.probe_val:
                if not self.original_g91: self.command.mdi("G90")
                pos = self.stat.position
                self.parent.add_log(self.resultname + " probe did not make contact at X%0.2f Y%0.2f Z%0.2f" % pos[:3])
                self.error = "Probe did not make contact"
            else:
                # Got initial contact, move slowly away to get most accurate position
                self.status = self.resultname + ': Probe away from surface'
                self.command.mdi("G91 G38.5 X%0.3f Y%0.3f Z%0.3f F%0.3f" %
                    (-self.probe_deltas[0], -self.probe_deltas[1], -self.probe_deltas[2], self.parent.latch_speed))
                self.step = 3
        
        elif self.step == 3:
            if self.stat.probe_val:
                self.error = self.resultname + ": Failed to probe away from surface!"
                return

            # Got accurate position, return to original position
            self.status = self.resultname + ': Return to original position'
            self.command.mdi("G90 G53 G0 X%0.3f Y%0.3f Z%0.3f F%0.3f" %
                (self.original_pos[0], self.original_pos[1], self.original_pos[2], self.parent.search_speed))
            self.step = 4
        
        elif self.step == 4:
            self.status = self.resultname + ': Complete'
            if self.original_g91: self.command.mdi("G91")
            self.result = list(self.stat.probed_position)

            # Adjust for probe ball diameter
            if self.probe_deltas[0] > 0: self.result[0] += self.parent.diameter / 2
            if self.probe_deltas[0] < 0: self.result[0] -= self.parent.diameter / 2
            if self.probe_deltas[1] > 0: self.result[1] += self.parent.diameter / 2
            if self.probe_deltas[1] < 0: self.result[1] -= self.parent.diameter / 2

            self.parent.set_result(self.resultname, self.result)

class ProbeHoleCenter:
    '''Probe hole center from inside, first determines
    center in X direction and then probes Y-/Y+/X-/X+.'''

    def __init__(self, parent, distance):
        self.parent = parent
        self.suboperation = None
        self.stat = self.parent.stat
        self.command = self.parent.command
        self.distance = distance
        self.step = 0
        self.status = ''
        self.error = None
    
    def __str__(self):
        if self.suboperation and self.suboperation.error:
            return self.suboperation.error
        elif self.done():
            return "Hole center probe done"
        else:
            return self.status

    def fraction(self):
        return self.step / 7.0

    def done(self):
        return self.error or (self.step == 7)

    def poll(self):
        if self.suboperation and not self.suboperation.done():
            self.suboperation.poll()

        elif self.suboperation and self.suboperation.error:
            self.error = self.suboperation.error
            
        elif self.error:
            return

        elif self.step == 0:
            self.status = 'Locate initial X center'
            self.suboperation = ProbeOperation(self.parent, "XMinus", [-self.distance, 0, 0])
            self.step = 1
        
        elif self.step == 1:
            self.suboperation = ProbeOperation(self.parent, "XPlus", [self.distance, 0, 0])
            self.step = 2
        
        elif self.step == 2:
            # Go to initial X center
            center = (self.parent.results['XMinus'][0] + self.parent.results['XPlus'][0]) / 2.0 - self.parent.offset_x
            self.command.mdi("G53 G0 X%0.3f F%0.3f" % (center, self.parent.search_speed))
            print("G53 G0 X%0.3f F%0.3f" % (center, self.parent.search_speed))
            self.command.wait_complete()

            self.status = 'Locate Y center'
            self.suboperation = ProbeOperation(self.parent, "YMinus", [0, -self.distance, 0])
            self.step = 3
        
        elif self.step == 3:
            self.suboperation = ProbeOperation(self.parent, "YPlus", [0, self.distance, 0])
            self.step = 4
        
        elif self.step == 4:
            # Go to measured Y center
            center = (self.parent.results['YMinus'][1] + self.parent.results['YPlus'][1]) / 2.0 - self.parent.offset_y
            self.command.mdi("G53 G0 Y%0.3f F%0.3f" % (center, self.parent.search_speed))
            self.command.wait_complete()

            # Probe more accurate X center now at the midline
            self.status = 'Locate X center'
            self.suboperation = ProbeOperation(self.parent, "XMinus", [-self.distance, 0, 0])
            self.step = 5
        
        elif self.step == 5:
            self.suboperation = ProbeOperation(self.parent, "XPlus", [self.distance, 0, 0])
            self.step = 6
        
        elif self.step == 6:
            # Go to measured center
            center_x = (self.parent.results['XMinus'][0] + self.parent.results['XPlus'][0]) / 2.0 - self.parent.offset_x
            center_y = (self.parent.results['YMinus'][1] + self.parent.results['YPlus'][1]) / 2.0 - self.parent.offset_y
            self.parent.add_log("Hole center: X %0.3f, Y %0.3f" % (center_x, center_y))
            self.command.mdi("G53 G0 X%0.3f Y%0.3f F%0.3f" % (center_x, center_y, self.parent.search_speed))
            self.command.wait_complete()
            self.step = 7

class ProbeGUI(object):
    def __init__(self, halcomp, builder, useropts):
        self.builder = builder
        self.command = linuxcnc.command()
        self.stat = linuxcnc.stat()
        self.update_offsets()

        glib.timeout_add(100, self.update_status)

        try:
            self.inifile = linuxcnc.ini(os.environ["INI_FILE_NAME"])
        except KeyError:
            self.inifile = None

        self.probe_distance = 20
        self.hole_radius = 50
        self.search_speed = 100
        self.latch_speed = 10
        self.diameter = 4
        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0
        if self.inifile:
            self.probe_distance = float(self.inifile.find("PROBE", "DISTANCE") or self.probe_distance)
            self.hole_radius = float(self.inifile.find("PROBE", "HOLERADIUS") or self.hole_radius)
            self.search_speed = float(self.inifile.find("PROBE", "SEARCH_SPEED") or self.search_speed)
            self.latch_speed = float(self.inifile.find("PROBE", "LATCH_SPEED") or self.latch_speed)
            self.diameter = float(self.inifile.find("PROBE", "DIAMETER") or self.diameter)
            self.offset_x = float(self.inifile.find("PROBE", "OFFSET_X") or self.offset_x)
            self.offset_y = float(self.inifile.find("PROBE", "OFFSET_Y") or self.offset_y)
            self.offset_z = float(self.inifile.find("PROBE", "OFFSET_Z") or self.offset_z)

        # Absolute coordinate results of latest probes
        self.results = {}
        self.prev_result_name = None

        # Currently running probe operation
        self.operation = None

    def onBtnXMinus(self, button, data = None):
        self.operation = ProbeOperation(self, 'XMinus', (-self.probe_distance, 0, 0))

    def onBtnXPlus(self, button, data = None):
        self.operation = ProbeOperation(self, 'XPlus', (self.probe_distance, 0, 0))

    def onBtnYMinus(self, button, data = None):
        self.operation = ProbeOperation(self, 'YMinus', (0, -self.probe_distance, 0))
    
    def onBtnYPlus(self, button, data = None):
        self.operation = ProbeOperation(self, 'YPlus', (0, self.probe_distance, 0))
    
    def onBtnZMinus(self, button, data = None):
        self.operation = ProbeOperation(self, 'ZMinus', (0, 0, -self.probe_distance))

    def onBtnHole(self, button, data = None):
        self.operation = ProbeHoleCenter(self, self.hole_radius)

    def onBtnZeroXMinus(self, button, data = None):
        self.setG5xOffset([self.results.get('XMinus')], 0, 0.0)

    def onBtnSetXMinus(self, button, data = None):
        self.setG5xOffset([self.results.get('XMinus')], 0,
            self.builder.get_object('sbXMinus').get_value())
    
    def onBtnZeroXPlus(self, button, data = None):
        self.setG5xOffset([self.results.get('XPlus')], 0, 0.0)

    def onBtnSetXPlus(self, button, data = None):
        self.setG5xOffset([self.results.get('XPlus')], 0,
            self.builder.get_object('adjXPlus').get_value())
    
    def onBtnZeroXCenter(self, button, data = None):
        self.setG5xOffset([self.results.get('XPlus'), self.results.get('XMinus')], 0, 0.0)

    def onBtnSetXCenter(self, button, data = None):
        self.setG5xOffset([self.results.get('XPlus'), self.results.get('XMinus')], 0,
            self.builder.get_object('adjXCenter').get_value())
    
    def onBtnZeroYMinus(self, button, data = None):
        self.setG5xOffset([self.results.get('YMinus')], 1, 0.0)

    def onBtnSetYMinus(self, button, data = None):
        self.setG5xOffset([self.results.get('YMinus')], 1,
            self.builder.get_object('adjYMinus').get_value())
    
    def onBtnZeroYPlus(self, button, data = None):
        self.setG5xOffset([self.results.get('YPlus')], 1, 0.0)

    def onBtnSetYPlus(self, button, data = None):
        self.setG5xOffset([self.results.get('YPlus')], 1,
            self.builder.get_object('adjYPlus').get_value())
    
    def onBtnZeroYCenter(self, button, data = None):
        self.setG5xOffset([self.results.get('YPlus'), self.results.get('YMinus')], 1, 0.0)

    def onBtnSetYCenter(self, button, data = None):
        self.setG5xOffset([self.results.get('YPlus'), self.results.get('YMinus')], 1,
            self.builder.get_object('adjYCenter').get_value())

    def onBtnZeroZMinus(self, button, data = None):
        self.setG5xOffset([self.results.get('ZMinus')], 2, 0.0)

    def onBtnSetZMinus(self, button, data = None):
        self.setG5xOffset([self.results.get('ZMinus')], 2,
            self.builder.get_object('adjZMinus').get_value())

    def setG5xOffset(self, points, axis_idx, value):
        '''Set G5x coordinate offset so that at the average of points,
        the given axis has the given value.'''
        if None in points:
             return

        axisname = 'XYZ'[axis_idx]
        avgpos = sum(p[axis_idx] for p in points) / float(len(points))

        self.command.mode(linuxcnc.MODE_MDI)
        self.command.wait_complete()
        self.command.mdi('G10 L2 P0 %s%0.3f' % (axisname, avgpos - value))
        self.command.wait_complete()
        self.update_status()

    def update_offsets(self):
        self.stat.poll()
        self.g5x_offset = list(self.stat.g5x_offset)
        self.g92_offset = list(self.stat.g92_offset)
        self.rotation = self.stat.rotation_xy

    def absolute_to_relative(self, point):
        '''Convert absolute coordinate to relative by applying current offsets.'''
        result = list(point[i] - self.g5x_offset[i] - self.g92_offset[i] for i in range(len(point)))
        if self.rotation != 0:
            angle = math.radians(self.rotation)
            x, y = result[:2]
            result[0] = x * math.cos(angle) - y * math.sin(angle)
            result[1] = x * math.sin(angle) + y * math.cos(angle)
        return result
    
    def update_label_text(self, widgetname, points, axis_idx):
        '''Format text for a result label.
        If multiple points are passed, uses the average position (center).
        '''
        if None not in points:
            relpoints = [self.absolute_to_relative(p) for p in points]
            avgpos = sum(p[axis_idx] for p in relpoints) / float(len(relpoints))
            text = '%+6.2f' % avgpos
        else:
            text = '-'
        widget = self.builder.get_object(widgetname)
        widget.set_text(text)

    def update_labels(self):
        self.update_label_text('lblXMinus', [self.results.get('XMinus')], 0)
        self.update_label_text('lblXPlus',  [self.results.get('XPlus')],  0)
        self.update_label_text('lblXCenter',[self.results.get('XMinus'),
                                             self.results.get('XPlus')],  0)
        self.update_label_text('lblYMinus', [self.results.get('YMinus')], 1)
        self.update_label_text('lblYPlus',  [self.results.get('YPlus')],  1)
        self.update_label_text('lblYCenter',[self.results.get('YMinus'),
                                             self.results.get('YPlus')],  1)
        self.update_label_text('lblZMinus', [self.results.get('ZMinus')], 2)
        
    def update_progressbar(self):
        progressbar = self.builder.get_object('progress')
        if self.operation:
            progressbar.set_fraction(self.operation.fraction())
            progressbar.set_text(str(self.operation))
        else:
            progressbar.set_fraction(0.0)
            progressbar.set_text("")
    
    def update_status(self):
        self.update_offsets()

        if self.operation:
            self.operation.poll()

        self.update_labels()
        self.update_progressbar()

        return True
    
    def add_log(self, msg):
        scroll = self.builder.get_object('swProbeLog')
        txtview = self.builder.get_object('txtProbeLog')
        buffer = txtview.get_property('buffer')
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        msg = timestamp + ": " + msg + '\n'

        iter = buffer.get_end_iter()
        if iter.get_line() > 1000:
            iter.set_line(1)
            buffer.delete(buffer.get_start_iter(), iter)
        
        buffer.insert(buffer.get_end_iter(), msg)
        
        scrollvert = scroll.get_vadjustment()
        scrollvert.set_value(scrollvert.get_upper())
        
    
    def set_result(self, result_name, point):
        x = point[0] + self.offset_x
        y = point[1] + self.offset_y
        z = point[2] + self.offset_z

        angletext = ''
        if result_name == prev_result_name:
            # Compute angle from previous measurement
            delta_x = x - self.results[result_name][0]
            delta_y = y - self.results[result_name][1]
            delta_z = z - self.results[result_name][2]
            
            # Choose reference axis based on probe direction
            if 'X' in result_name:
                angle = math.atan(delta_x / delta_y)
            elif 'Y' in result_name:
                angle = math.atan(-delta_y / delta_x)
            elif 'Z' in result_name:
                angle = math.atan(delta_z / math.sqrt(delta_x**2 + delta_y**2))

            angletext = ' Angle %0.3f deg' % (math.degrees(angle))

        self.add_log(result_name + " result X %0.3f Y %0.3f Z %0.3f" % (x, y, z) + angletext)
        self.results[result_name] = [x, y, z]
        self.prev_result_name = result_name
    
def get_handlers(halcomp, builder, useropts):
    return [ProbeGUI(halcomp, builder, useropts)]
            
