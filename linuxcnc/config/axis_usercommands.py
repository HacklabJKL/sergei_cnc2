# # Embed qtvcp side panel
# from subprocess import Popen
# qtvcp_frame = Tkinter.Frame(root_window, width = 150, container=1,
#                             borderwidth=0, highlightthickness=0)
# qtvcp_frame.grid(row=0, column=4, rowspan=6, sticky="nsew", padx=4, pady=4)
# xid = qtvcp_frame.winfo_id()
# cmd = ["/usr/bin/qtvcp", "-x", str(xid), "qtvcp_sidepanel.ui"]
# child = Popen(cmd)
# _dynamic_childs["qtvcp_sidepanel"] = (child, cmd, False)

# Unbind keyboard commands (prefer physical buttons)
for key in root_window.bind():
    root_window.unbind(key)
root_window.bind_class("all", "<Key-F1>", '')

# Maximize window
maxgeo=root_window.tk.call("wm","maxsize",".")
fullsize=str(maxgeo[0]) + 'x' + str(maxgeo[1])
root_window.tk.call("wm","geometry",".",fullsize)

# Customize tab titles
root_window.tk.call('.pane.top.tabs','itemconfigure','manual','-text','Manual control')
root_window.tk.call('.pane.top.tabs','itemconfigure','mdi','-text','Manual G-code')

# Reduce tab widths
root_window.tk.call('.pane.top.tabs', 'configure', '-width', '50')
root_window.tk.call('.pane.top.maxvel.l0', 'configure', '-text', 'Max Speed:')
manual_tab = root_window.tk.call('.pane.top.tabs', 'getframe', 'manual')
root_window.tk.call('grid', 'forget', manual_tab + '.jogf.zerohome.tooltouch')

class DisplayUpdate:
    def __init__(self):
        self.prev_id = 0

    def hal_pins(self, comp):
        self.comp = comp
        comp.newpin("display-update-count", hal.HAL_U32, hal.HAL_OUT)
        comp["display-update-count"] = 0

        comp.newpin("extents-minx", hal.HAL_FLOAT, hal.HAL_OUT)
        comp.newpin("extents-miny", hal.HAL_FLOAT, hal.HAL_OUT)
        comp.newpin("extents-minz", hal.HAL_FLOAT, hal.HAL_OUT)
        comp.newpin("extents-maxx", hal.HAL_FLOAT, hal.HAL_OUT)
        comp.newpin("extents-maxy", hal.HAL_FLOAT, hal.HAL_OUT)
        comp.newpin("extents-maxz", hal.HAL_FLOAT, hal.HAL_OUT)
        comp["extents-minx"] = 0.0
        comp["extents-miny"] = 0.0
        comp["extents-minz"] = 0.0
        comp["extents-maxx"] = 0.0
        comp["extents-maxy"] = 0.0
        comp["extents-maxz"] = 0.0

    def update(self):
        if self.prev_id != id(o.canon):
            self.prev_id = id(o.canon)
            self.comp["display-update-count"] = comp["display-update-count"] + 1

            minext = from_internal_units(o.canon.min_extents)
            maxext = from_internal_units(o.canon.max_extents)

            self.comp["extents-minx"] = minext[0]
            self.comp["extents-miny"] = minext[1]
            self.comp["extents-minz"] = minext[2]
            self.comp["extents-maxx"] = maxext[0]
            self.comp["extents-maxy"] = maxext[1]
            self.comp["extents-maxz"] = maxext[2]

displayupdate = DisplayUpdate()

def user_hal_pins():
    displayupdate.hal_pins(comp)


# Show remaining time in LinuxCNC Axis status bar
# Place this code in your axis_usercommands.py
class RemainingTime:
    prev_update = 0         # Previous time user_live_update() was called
    prev_calculate = None   # Hash of preview gcode state, to avoid unnecessary recalculations
    prev_line = 0           # Previous executed G-code line
    total_feed = 0          # Total feed time (seconds) in program at normal speed
    total_traverse = 0      # Total traverse time (seconds) in program at normal speed
    total_dwell = 0         # Total dwell time in program
    done_feed = 0           # Feed time (seconds) done so far at normal speed
    done_traverse = 0       # Traverse time (seconds) done so far at normal speed
    done_dwell = 0          # Total dwell time done so far
    first_traverse = 0      # Ignore first traverse to the G-code start position

    def __init__(self):
        self.info = nf.makewidget(root_window, Frame, '.info')
        tool_label = nf.makewidget(root_window, Label, '.info.tool')
        tool_label.pack_forget()
        self.label = Tkinter.Label(self.info, text="Foobar", anchor="w", borderwidth=2, relief="sunken", width=30)
        self.label.pack(fill="x", side="left", expand=1)
        tool_label.pack(side="left")

        # Get maximum velocity per each axis
        # GLCanon works in inches so convert the unit
        self.velocity_to_inch_per_s = 1 / 25.4
        self.max_vels = [
            float(inifile.find('AXIS_X', 'MAX_VELOCITY')) * self.velocity_to_inch_per_s,
            float(inifile.find('AXIS_Y', 'MAX_VELOCITY')) * self.velocity_to_inch_per_s,
            float(inifile.find('AXIS_Z', 'MAX_VELOCITY')) * self.velocity_to_inch_per_s
        ]
        self.max_accels = [
            float(inifile.find('AXIS_X', 'MAX_ACCELERATION')) * self.velocity_to_inch_per_s,
            float(inifile.find('AXIS_Y', 'MAX_ACCELERATION')) * self.velocity_to_inch_per_s,
            float(inifile.find('AXIS_Z', 'MAX_ACCELERATION')) * self.velocity_to_inch_per_s
        ]

    def segment_time(self, start, end, feed):
        '''Calculate time taken by a segment, roughly approximating velocity
        and acceleration effects.
        '''
        # Calculate velocity vector
        delta = (end[0]-start[0], end[1]-start[1], end[2]-start[2])
        distance = sum(x**2 for x in delta)**0.5

        if distance <= 1e-6:
            return 0.0
        
        velocity = tuple(feed * x / distance for x in delta)

        # Compare against axis max velocities
        velocity_factor = min((abs(x / y) if x < abs(y) else 1.0) for x, y in zip(self.max_vels, velocity))
        if velocity_factor < 1.0:
            velocity = tuple(x * velocity_factor for x in velocity)

        # Compute acceleration time
        # This is not perfectly accurate because it doesn't take into account
        # path blending, and also we receive the feed vs. traverse segments
        # in wrong order. But it gets close.
        velocity_delta = tuple(abs(x - y) for x, y in zip(velocity, self.velocity))
        accel_time = max(x / y for x, y in zip(velocity_delta, self.max_accels))
        self.velocity = velocity

        try:
            return distance / (feed * velocity_factor) + accel_time
        except ZeroDivisionError:
            return 0.0

    def update_total_time(self):
        '''Calculate total time for G-code based on loaded preview'''

        # Get traverse velocity in inches per second
        maxvel = live_plotter.stat.max_velocity * self.velocity_to_inch_per_s

        # Check if anything has changed
        canon = o.canon
        key = hash((id(canon), maxvel))
        if key == self.prev_calculate: return
        self.prev_calculate = key

        # Add up estimated times for each segment
        self.total_traverse = 0
        self.total_feed = 0
        self.total_dwell = canon.dwell_time
        self.velocity = (0,0,0)
        for seg in canon.traverse:
            self.total_traverse += self.segment_time(seg[1][:3], seg[2][:3], maxvel)

        for seg in canon.feed:
            self.total_feed += self.segment_time(seg[1][:3], seg[2][:3], seg[3])

        for seg in canon.arcfeed:
            self.total_feed += self.segment_time(seg[1][:3], seg[2][:3], seg[3])

    def format_time(self, seconds):
        if seconds > 120:
            return '%.0f min' % (seconds / 60.0)
        else:
            return '%.0f sec' % seconds

    def update(self):
        t = time.time()
        delta = t - self.prev_update
        self.prev_update = t

        self.update_total_time()
        stat = live_plotter.stat

        if stat.task_mode == linuxcnc.MODE_AUTO:
            # Count the time spent feeding / traversing
            if stat.paused:
                pass
            elif stat.motion_type == linuxcnc.MOTION_TYPE_TRAVERSE:
                if self.first_traverse is None or self.first_traverse == stat.id:
                    self.first_traverse = stat.id
                    pass # Ignore the traverse to G-code start position
                else:
                    self.done_traverse += delta * stat.rapidrate
            elif stat.motion_type != 0:
                self.first_traverse = -1
                self.done_feed += delta * stat.feedrate

            elif stat.delay_left > 0:
                self.done_dwell += delta

            progress_percent = 100 * ((self.done_traverse + self.done_feed + self.done_dwell) /
                                      (self.total_traverse + self.total_feed + self.total_dwell))
            try:
                remain = ((self.total_traverse - self.done_traverse) / stat.rapidrate
                        + (self.total_feed - self.done_feed) / stat.feedrate
                        + (self.total_dwell - self.done_dwell))
            except ZeroDivisionError:
                remain = float("inf")

            self.label['text'] = 'Progress: %0.1f %% (remaining %s)' % (progress_percent, self.format_time(remain))
        else:
            # In manual mode
            self.done_traverse = self.done_feed = self.done_dwell = 0
            self.first_traverse = None
            try:
                remain = (self.total_traverse / stat.rapidrate + self.total_feed / stat.feedrate + self.total_dwell)
            except ZeroDivisionError:
                remain = self.total_traverse + self.total_feed
            self.label['text'] = 'Estimated run time %s' % (self.format_time(remain),)


remainingtime = RemainingTime()
def user_live_update():
    remainingtime.update()
    displayupdate.update()
