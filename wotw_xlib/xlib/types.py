# pylint: disable=invalid-name,too-few-public-methods
"""This file collects several X11 types"""

from ctypes import c_char_p, c_int, c_long, c_uint, c_ulong, POINTER, Structure


class Display(Structure):
    """
    The display class is just a placeholder. For the most part, X11 doesn't
    want you to touch Display.

    see: https://github.com/mirror/libX11/blob/libX11-1.6.5/include/X11/Xlib.h#L484
    > A Display should be treated as opaque by application code
    """
    _fields_ = [
        ('_opaque_struct', c_int)
    ]

Window = c_ulong
Coordinate = c_int

# Window map state, which comes from the docs below:
# https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
IsUnmapped = 0
IsUnviewable = 1
IsViewable = 2

IGNORED_FOR_NOW = POINTER(c_int)


class XTextProperty(Structure):
    """
    This structure was hastily thrown together to access WM Icon Names

    see: https://tronche.com/gui/x/xlib/ICC/client-to-window-manager/converting-string-lists.html
    """
    _fields_ = [
        ('value', c_char_p),
        ('encoding', IGNORED_FOR_NOW),
        ('format', c_int),
        ('nitems', c_ulong)
    ]


class XWindowAttributes(Structure):
    """
    This struct contains several useful things and several things I don't use
    at the moment.

    see: https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
    """
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
