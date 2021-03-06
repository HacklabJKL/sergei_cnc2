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

# For probe screen
# Copyright (c) 2020 Probe Screen NG Developers
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

# This AXIS RC file adds support for an error pin, mirroring the
# gmocappy.error pin's behaviour for AXIS.


def _remaining_error_count(widgets):
    """ Returns the count of remaining error messages """
    count = 0
    for i, item in enumerate(widgets):
        frame, icon, text, button, iname = item
        if iname == "icon_std_error":
            count += 1
    return count


def my_add(self, iconname, message):
    """ Signal to PSNG that an error has occurred. """
    self.original_add(iconname, message)

    if iconname == "error":
        probe_user_comp["error"] = True


def my_remove(self, widgets):
    """ Signal to PSNG when all errors have been cleared. """
    self.original_remove(widgets)

    if _remaining_error_count(self.widgets) == 0:
        probe_user_comp["error"] = False


# Rename the original add/remove method so we can retain the ability to call them
Notification.original_add = Notification.add
Notification.original_remove = Notification.remove

# Replace the add/remove methods with a wrapped version that manages an error pin
Notification.add = my_add
Notification.remove = my_remove

if hal_present == 1:
    # Add an probe.user.error pin
    probe_user_comp = hal.component("probe.user")
    probe_user_comp.newpin("error", hal.HAL_BIT, hal.HAL_OUT)
    probe_user_comp.ready()