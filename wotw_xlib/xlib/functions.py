# pylint: disable=invalid-name
"""This file collects several X11 functions"""

from ctypes import CDLL, c_char_p, c_int, c_uint, c_ulong, POINTER

from wotw_xlib.xlib.types import Coordinate, Display, Window, XWindowAttributes, XTextProperty

lib = CDLL('libX11.so.6')

XCloseDisplay = lib.XCloseDisplay
XCloseDisplay.argtypes = [POINTER(Display)]
XCloseDisplay.restype = c_int

XDefaultScreen = lib.XDefaultScreen
XDefaultScreen.argtypes = [POINTER(Display)]
XDefaultScreen.restype = c_int

XGetGeometry = lib.XGetGeometry
XGetGeometry.argtypes = [
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
XGetGeometry.restype = c_int

XGetWindowAttributes = lib.XGetWindowAttributes
XGetWindowAttributes.argtypes = [
    POINTER(Display),
    Window,
    POINTER(XWindowAttributes)
]
XGetWindowAttributes.restype = c_int

XGetWMIconName = lib.XGetWMIconName
XGetWMIconName.argtypes = [
    POINTER(Display),
    Window,
    POINTER(XTextProperty)
]
XGetWMIconName.restype = c_int

XOpenDisplay = lib.XOpenDisplay
XOpenDisplay.argtypes = [c_char_p]
XOpenDisplay.restype = POINTER(Display)

XQueryPointer = lib.XQueryPointer
XQueryPointer.argtypes = [
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
XQueryPointer.restype = c_int

XQueryTree = lib.XQueryTree
XQueryTree.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Window),
    POINTER(POINTER(Window)),
    POINTER(c_uint)
]
XQueryTree.restype = c_int

XRootWindow = lib.XRootWindow
XRootWindow.argtypes = [POINTER(Display), c_int]
XRootWindow.restype = Window

XFetchName = lib.XFetchName
XFetchName.argtypes = [POINTER(Display), Window, POINTER(c_char_p)]
XFetchName.restype = c_int
