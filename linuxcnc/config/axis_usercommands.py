# # Embed qtvcp side panel
# from subprocess import Popen
# qtvcp_frame = Tkinter.Frame(root_window, width = 150, container=1,
#                             borderwidth=0, highlightthickness=0)
# qtvcp_frame.grid(row=0, column=4, rowspan=6, sticky="nsew", padx=4, pady=4)
# xid = qtvcp_frame.winfo_id()
# cmd = ["/usr/bin/qtvcp", "-x", str(xid), "qtvcp_sidepanel.ui"]
# child = Popen(cmd)
# _dynamic_childs["qtvcp_sidepanel"] = (child, cmd, False)

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

    def update_total_time(self):
        '''Calculate total time for G-code based on loaded preview'''

        # Check if anything has changed
        maxvel = live_plotter.stat.max_velocity
        canon = o.canon
        key = hash((id(canon), maxvel))
        if key == self.prev_calculate: return
        self.prev_calculate = key

        self.total_traverse = sum(dist(l[1][:3], l[2][:3]) / maxvel for l in canon.traverse)
        self.total_feed = (sum(dist(l[1][:3], l[2][:3]) / min(maxvel, l[3]) for l in canon.feed) +
                           sum(dist(l[1][:3], l[2][:3]) / min(maxvel, l[3]) for l in canon.arcfeed))
        self.total_dwell = canon.dwell_time

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
