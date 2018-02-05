# pylint: disable=too-many-function-args
"""This file provides NeedsDisplay, a class to collect display tooling"""

from ctypes import c_char_p


from wotw_xlib.xlib import Display, XCloseDisplay, XOpenDisplay


class NeedsDisplay(object):
    """This class provides the vehicle to manage a Display connection"""

    def __init__(self, unknown_display=None):
        """Ctor initializes the display state"""
        self.opened_display = False
        self.display = self.parse_unknown_display(unknown_display)

    def parse_unknown_display(self, unknown_display=None):
        """
        This method checks for an existing display and viable display strings
        """
        if isinstance(unknown_display, Display):
            return unknown_display
        if not isinstance(unknown_display, (basestring, c_char_p)):
            unknown_display = None
        return self.open_display(unknown_display)

    def open_display(self, display_to_open):
        """Sets an internal flag and returns the display"""
        self.opened_display = True
        return XOpenDisplay(display_to_open)

    def close_display(self):
        """Checks the internal flag and only closes displays it opened"""
        if self.opened_display:
            XCloseDisplay(self.display)

    def __enter__(self):
        """Sends itself off"""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Explicitly closes the display"""
        self.close_display()
