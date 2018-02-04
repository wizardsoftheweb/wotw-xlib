# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import print_function

from ctypes import byref, CDLL, c_char_p, c_int, c_long, c_uint, c_ulong, POINTER, Structure
from logging import addLevelName, Formatter, getLogger, INFO, StreamHandler
from sys import exit as sys_exit, stderr
from time import time as time_now

SILLY = 5
addLevelName(SILLY, 'SILLY')
LOGGER = getLogger('wotw-macro')
CONSOLE_HANDLER = StreamHandler(stream=stderr)
CONSOLE_FORMATTER = Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.silly = (
    lambda message, *args, **kwargs:
    LOGGER.log(SILLY, message, *args, **kwargs)
)
LOGGER.setLevel(INFO)

# from pyglet.libs.x11 import xlib

xlib = CDLL('libX11.so.6')


class Display(Structure):
    # https://github.com/mirror/libX11/blob/libX11-1.6.5/include/X11/Xlib.h#L484
    # A Display should be treated as opaque by application code
    _fields_ = [
        ('_opaque_struct', c_int)
    ]

Window = c_ulong
Coordinate = c_int

# https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
# int map_state;          /* IsUnmapped, IsUnviewable, IsViewable */
IsUnmapped = 0
IsUnviewable = 1
IsViewable = 2

IGNORED_FOR_NOW = POINTER(c_int)


class XTextProperty(Structure):
    # https://tronche.com/gui/x/xlib/ICC/client-to-window-manager/converting-string-lists.html
    _fields_ = [
        ('value', c_char_p),
        ('encoding', IGNORED_FOR_NOW),
        ('format', c_int),
        ('nitems', c_ulong)
    ]


class XWindowAttributes(Structure):
    # https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
    _fields_ = [
        ('x', Coordinate),
        ('y', Coordinate),
        ('width', c_uint),
        ('height', c_uint),
        ('border_width', c_uint),
        ('depth', c_uint),
        ('visual', IGNORED_FOR_NOW),
        ('root', Window),
        ('class', c_int),
        ('bit_gravity', c_int),
        ('win_gravity', c_int),
        ('backing_store', c_int),
        ('backing_planes', c_ulong),
        ('backing_pixel', c_ulong),
        ('save_under', c_int),
        ('colormap', IGNORED_FOR_NOW),
        ('map_installed', c_int),
        ('map_state', c_int),
        ('all_event_masks', c_long),
        ('your_event_mask', c_long),
        ('do_not_propagate_mask', c_long),
        ('override_redirect', c_int),
        ('screen', IGNORED_FOR_NOW),
    ]

xlib.XOpenDisplay.argtypes = [c_char_p]
xlib.XOpenDisplay.restype = POINTER(Display)
xlib.XDefaultScreen.argtypes = [POINTER(Display)]
xlib.XDefaultScreen.restype = c_int
xlib.XRootWindow.argtypes = [POINTER(Display), c_int]
xlib.XRootWindow.restype = Window
xlib.XQueryPointer.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Window),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(c_ulong)
]
xlib.XQueryPointer.restype = c_int
xlib.XQueryTree.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Window),
    POINTER(POINTER(Window)),
    POINTER(c_uint)
]
xlib.XQueryTree.restype = c_int
xlib.XGetGeometry.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(c_uint),
    POINTER(c_uint),
    POINTER(c_uint),
    POINTER(c_uint)
]
xlib.XGetGeometry.restype = c_int
xlib.XGetWindowAttributes.argtypes = [
    POINTER(Display),
    Window,
    POINTER(XWindowAttributes)
]
xlib.XGetWindowAttributes.restype = c_int
xlib.XCloseDisplay.argtypes = [POINTER(Display)]
xlib.XCloseDisplay.restype = c_int
xlib.XFetchName.argtypes = [POINTER(Display), Window, POINTER(c_char_p)]
xlib.XFetchName.restype = c_int
xlib.XGetWMIconName.argtypes = [
    POINTER(Display),
    Window,
    POINTER(XTextProperty)
]
xlib.XGetWMIconName.restype = c_int


class Point(object):

    def __init__(self, x, y):
        self.x = self.parse_coordinate(x)
        self.y = self.parse_coordinate(y)

    @staticmethod
    def parse_coordinate(raw_coordinate):
        return (
            raw_coordinate.value
            if hasattr(raw_coordinate, 'value')
            else raw_coordinate
        )

    def is_above_and_left_of(self, unknown_point):
        return (
            self.x <= unknown_point.x
            and
            self.y <= unknown_point.y
        )

    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)


class Region(object):

    def __init__(self, top_left, width=0, height=0):
        self.top_left = top_left
        self.bottom_right = Point(
            self.top_left.x + Point.parse_coordinate(width),
            self.top_left.y + Point.parse_coordinate(height)
        )

    def contains(self, unknown_point):
        return (
            self.top_left.is_above_and_left_of(unknown_point)
            and
            unknown_point.is_above_and_left_of(self.bottom_right)
        )

    def __str__(self):
        return "%sx%s" % (self.top_left, self.bottom_right)


def benchmark(method_to_benchmark, *args, **kwargs):
    start = time_now()
    method_to_benchmark(*args, **kwargs)
    end = time_now()
    return end - start


def gather_basics(display_index=None):
    LOGGER.info('Gathering display and root window')
    LOGGER.debug("Display index: %s", display_index)
    display = xlib.XOpenDisplay(display_index)
    LOGGER.debug("Display: %s", display)
    screen = xlib.XDefaultScreen(display)
    LOGGER.debug("Screen: %s", screen)
    root_window = xlib.XRootWindow(display, screen)
    LOGGER.debug("Root Window: %s", root_window)
    return [display, root_window]


def whoops(display, call, result):
    LOGGER.error("%s isn't truthy", result)
    LOGGER.critical("Something went wrong with %s", call)
    close_the_display(display)


def get_mouse_position(display, root_window):
    LOGGER.debug(
        "Determining mouse position relative to window %s",
        root_window
    )
    (root_reference, parent_reference) = (Window(), Window())
    (root_x, root_y) = (Coordinate(), Coordinate())
    (win_x, win_y) = (Coordinate(), Coordinate())
    mask = c_ulong()
    result = xlib.XQueryPointer(
        display,
        root_window,
        byref(root_reference),
        byref(parent_reference),
        byref(root_x),
        byref(root_y),
        byref(win_x),
        byref(win_y),
        byref(mask)
    )
    if not result:
        whoops(display, 'XQueryPointer', result)
    root_point = Point(root_x, root_y)
    LOGGER.silly("Root location: %s", root_point)
    window_point = Point(win_x, win_y)
    LOGGER.silly("Window location: %s", window_point)
    return [root_point, window_point]


def get_window_region(display, window):
    LOGGER.debug("Determining region for window %s", window)
    window_reference = Window()
    (win_x, win_y) = (Coordinate(), Coordinate())
    (width, height) = (c_uint(), c_uint())
    border_width = c_uint()
    depth = c_uint()
    result = xlib.XGetGeometry(
        display,
        window,
        byref(window_reference),
        byref(win_x),
        byref(win_y),
        byref(width),
        byref(height),
        byref(border_width),
        byref(depth)
    )
    if not result:
        whoops(display, 'XGetGeometry', result)
    win_region = Region(
        Point(win_x, win_y),
        width,
        height
    )
    LOGGER.silly("Window %s Region: %s", window, win_region)
    return win_region


def window_region_contains_pointer(display, window, pointer_location):
    LOGGER.debug("Checking if window %s contains the pointer", window)
    win_region = get_window_region(display, window)
    contained = win_region.contains(pointer_location)
    LOGGER.silly(
        "Window %s does%s contain %s",
        window,
        (
            '' if contained
            else ' not'
        ),
        pointer_location
    )
    return contained


def window_is_viewable(win_attributes):
    LOGGER.debug('Checking if window is viewable')
    viewable = win_attributes.map_state == IsViewable
    LOGGER.silly(
        "Window is%s viewable",
        (
            '' if viewable
            else ' not'
        )
    )
    return viewable


def get_window_attributes(display, window):
    LOGGER.debug("Getting attributes for window %s", window)
    win_attributes = XWindowAttributes()
    result = xlib.XGetWindowAttributes(display, window, byref(win_attributes))
    if not result:
        whoops(display, 'XGetWindowAttributes', result)
    return win_attributes


def window_might_be_on_top(display, window):
    LOGGER.debug("Checking if window %s is near the top", window)
    win_attributes = get_window_attributes(display, window)
    return window_is_viewable(win_attributes)


def window_contains_pointer_and_is_on_top(display, window, pointer_location):
    return (
        window_region_contains_pointer(display, window, pointer_location)
        and
        window_might_be_on_top(display, window)
    )


def get_window_tree(display, root_window):
    LOGGER.debug("Parsing the window tree from %s", root_window)
    (root_reference, parent_reference) = (Window(), Window())
    child_pointers = POINTER(Window)()
    number_of_children = c_uint()
    result = xlib.XQueryTree(
        display,
        root_window,
        byref(root_reference),
        byref(parent_reference),
        byref(child_pointers),
        byref(number_of_children)
    )
    if not result:
        whoops(display, 'XQueryTree', result)
    LOGGER.silly("Discovered %d children", number_of_children.value)
    return [child_pointers, number_of_children]


def get_window_under_pointer(display, root_window):
    LOGGER.silly(
        "Searching for the window under the pointer relative to window %s",
        root_window
    )
    pointers, total_count = get_window_tree(display, root_window)
    if total_count.value > 0:
        discovered_window = root_window
        pointer_location = get_mouse_position(display, root_window)[1]
        # The topmost window will be the lowest in the XQueryTree
        # (which is untested and needs proof)
        for index in range(0, total_count.value):
            if window_contains_pointer_and_is_on_top(display, pointers[index], pointer_location):
                discovered_window = pointers[index]
                LOGGER.silly("Window %s might be the target",
                             discovered_window)
        if discovered_window != root_window:
            return get_window_under_pointer(display, discovered_window)
    LOGGER.debug("No other viable children found; returning %s", root_window)
    return root_window


def get_window_names(display, window):
    LOGGER.debug("Naming window %s", window)
    name = c_char_p()
    xlib.XFetchName(display, window, byref(name))
    LOGGER.silly("WM Name: %s", name.value)
    props = XTextProperty()
    xlib.XGetWMIconName(display, window, byref(props))
    LOGGER.silly("WM Icon Name: %s", props.value)
    return [name.value, props.value]


def parse_names(first, second):
    LOGGER.debug("Comparing %s and %s", first, second)
    if first == second or len(first) > len(second):
        LOGGER.silly('Chose the first; same string or same length')
        return first
    LOGGER.silly('Chose the second; first is not equal and shorter')
    return second


def close_the_display(display):
    LOGGER.info("Closing the display")
    xlib.XCloseDisplay(display)


def find_window():
    LOGGER.info('Launching')
    display, root_window = gather_basics()
    LOGGER.info('Beginning search')
    window = get_window_under_pointer(display, root_window)
    LOGGER.info("Window candidate is %s", window)
    names = get_window_names(display, window)
    probable_window_name = parse_names(*names)
    LOGGER.info("Picked %s", probable_window_name)
    close_the_display(display)


def display_benchmark(method_to_benchmark, *args, **kwargs):
    run_length = benchmark(method_to_benchmark, *args, **kwargs)
    milli_run_length = run_length * 1000
    LOGGER.info(
        """Wrapping up
        Runtime
        {: >14}: {: > 10.4f}
        {: >14}: {: > 10.4f}
        {: >14}: {: > 10.4f}
        {: >14}: {: > 5d}
        """.format(
            'seconds', run_length,
            'milliseconds', milli_run_length,
            'microseconds', milli_run_length * 1000,
            'Ops per second',
            int(1000 / milli_run_length)
        )
    )


def cli():
    display_benchmark(find_window)
    sys_exit(0)

if '__main__' == __name__:
    cli()
