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
