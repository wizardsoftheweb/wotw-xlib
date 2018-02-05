"""This files provides a common interface for window/pointer interaction"""

from ctypes import byref, c_char_p, c_uint, c_ulong, POINTER

from wotw_xlib.utils import Point, Region
from wotw_xlib.xlib import (
    Coordinate,
    IsViewable,
    Window,
    XDefaultScreen,
    XFetchName,
    XGetGeometry,
    XGetWMIconName,
    XGetWindowAttributes,
    XQueryPointer,
    XQueryTree,
    XRootWindow,
    XTextProperty,
    XWindowAttributes
)
from wotw_xlib.common import NeedsDisplay


class PointerWindow(NeedsDisplay):
    """This class collects methods to inspect pointer position on the display"""

    def __init__(self, display=None, window_id=None):

        super(PointerWindow, self).__init__(display)
        self.window = self.parse_window_id(window_id)
        self.region = self.get_region()
        self.window_attributes = None

    def parse_window_id(self, window_id=None):
        """Return the passed in ID or find the root window"""
        if isinstance(window_id, Window):
            return window_id
        return self.discover_root_window()

    def discover_root_window(self):
        """Gets the root window for the screen"""
        screen = XDefaultScreen(self.display)
        return XRootWindow(self.display, screen)

    def get_mouse_position(self):
        """Gets the mouse position relative to the display and window"""
        (root_x, root_y) = (Coordinate(), Coordinate())
        (win_x, win_y) = (Coordinate(), Coordinate())
        XQueryPointer(
            self.display,
            self.window,
            Window(),
            Window(),
            byref(root_x),
            byref(root_y),
            byref(win_x),
            byref(win_y),
            c_ulong()
        )
        return [Point(root_x, root_y), Point(win_x, win_y)]

    def get_region(self):
        """Returns the window's region"""
        (win_x, win_y) = (Coordinate(), Coordinate())
        (width, height) = (c_uint(), c_uint())
        XGetGeometry(
            self.display,
            self.window,
            Window(),
            byref(win_x),
            byref(win_y),
            byref(width),
            byref(height),
            c_uint(),
            c_uint()
        )
        return Region(
            Point(win_x, win_y),
            width,
            height
        )

    def get_window_attributes(self):
        """Collects the window attributes"""
        win_attributes = XWindowAttributes()
        XGetWindowAttributes(
            self.display,
            self.window,
            byref(win_attributes)
        )
        return win_attributes

    def get_names(self):
        """Collects the WM Name and WM Icon Name"""
        name = c_char_p()
        XFetchName(self.display, self.window, byref(name))
        props = XTextProperty()
        XGetWMIconName(self.display, self.window, byref(props))
        return [name.value, props.value]

    def get_query_tree(self):
        """Gets the window tree from the specified root"""
        child_pointers = POINTER(Window)()
        number_of_children = c_uint()
        XQueryTree(
            self.display,
            self.window,
            Window(),
            Window(),
            byref(child_pointers),
            byref(number_of_children)
        )
        return [child_pointers, number_of_children.value]

    def contains_pointer(self, pointer_location=None):
        """Checks to see if the window might contain the pointer"""
        # If the location isn't specified, we must want relative
        # On the root window, that works out well
        if pointer_location is None:
            pointer_location = self.get_mouse_position()[1]
        return self.region.contains(pointer_location)

    def is_viewable(self):
        """Checks if the Window is reporting an obstruction"""
        if not self.window_attributes:
            self.window_attributes = self.get_window_attributes()
        return self.window_attributes.map_state == IsViewable

    def might_be_under_pointer(self, pointer_location=None):
        """
        Test if the window region could contain the pointer and if the window is
        viewable
        """
        if self.contains_pointer(pointer_location):
            return self.is_viewable()
        return False
