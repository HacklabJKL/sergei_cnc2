import sys
import os
import linuxcnc

from PyQt5 import QtCore, QtWidgets

# from qtvcp.widgets.mdi_line import MDILine as MDI_WIDGET
# from qtvcp.widgets.gcode_editor import GcodeEditor as GCODE
# from qtvcp.widgets.stylesheeteditor import  StyleSheetEditor as SSE
# from qtvcp.lib.keybindings import Keylookup
# from qtvcp.core import Status, Action

# Set up logging
# from qtvcp import logger
# LOG = logger.getLogger(__name__)
# LOG.setLevel(logger.INFO) # One of DEBUG, INFO, WARNING, ERROR, CRITICAL


class HandlerClass:
    def __init__(self, halcomp,widgets,paths):
        self.hal = halcomp
        self.w = widgets
        self.PATHS = paths

    def initialized__(self):
        pass

    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)

def get_handlers(halcomp,widgets,paths):
     return [HandlerClass(halcomp,widgets,paths)]
