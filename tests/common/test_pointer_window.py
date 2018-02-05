# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

# from ctypes import c_char_p
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_xlib.utils import Point
from wotw_xlib.common import PointerWindow
# pylint:disable=unused-import
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
# pylint:enable=unused-import


class PointerWindowTestCase(TestCase):
    DEFAULT_DISPLAY = None
    DEFAULT_SCREEN = '2'
    PARSED_DISPLAY = 'a display'
    DEFAULT_WINDOW_ID = 47

    def setUp(self):
        self.construct_pointer_window()

    def wipe_pointer_window(self):
        del self.pointer_window

    def construct_pointer_window(self):
        super_patcher = patch(
            'wotw_xlib.common.pointer_window.super',
            return_value=MagicMock()
        )
        self.mock_super = super_patcher.start()
        parse_window_id_patcher = patch.object(
            PointerWindow,
            'parse_window_id'
        )
        self.mock_parse_window_id = parse_window_id_patcher.start()
        get_region_patcher = patch.object(PointerWindow, 'get_region')
        self.mock_get_region = get_region_patcher.start()
        self.pointer_window = PointerWindow(
            self.DEFAULT_DISPLAY,
            self.DEFAULT_WINDOW_ID
        )
        self.pointer_window.display = self.DEFAULT_DISPLAY
        parse_window_id_patcher.stop()
        get_region_patcher.stop()
        super_patcher.stop()
        self.addCleanup(self.wipe_pointer_window)


class ConstructorUnitTests(PointerWindowTestCase):

    def test_super_called(self):
        self.mock_super.assert_called_once()

    def test_window_parsed(self):
        self.mock_parse_window_id.assert_called_once_with(
            self.DEFAULT_WINDOW_ID
        )

    def test_region_created(self):
        self.mock_get_region.assert_called_once_with()

    def test_window_attributes_are_empty(self):
        self.assertIsNone(self.pointer_window.window_attributes)


class ParseWindowIdUnitTests(PointerWindowTestCase):

    @patch(
        'wotw_xlib.common.PointerWindow.discover_root_window',
        return_value=MagicMock()
    )
    def test_with_window(self, mock_discover):
        test_window = Window(self.DEFAULT_WINDOW_ID)
        result = self.pointer_window.parse_window_id(test_window)
        self.assertEquals(result, test_window)
        self.assertEquals(mock_discover.call_count, 0)

    @patch(
        'wotw_xlib.common.PointerWindow.discover_root_window',
        return_value=MagicMock()
    )
    def test_without_window(self, mock_discover):
        test_window = 'qqq'
        result = self.pointer_window.parse_window_id(test_window)
        self.assertNotEquals(result, test_window)
        mock_discover.assert_called_once_with()


class DiscoverRootWindowUnitTests(PointerWindowTestCase):

    @patch(
        'wotw_xlib.common.pointer_window.XDefaultScreen',
        return_value=PointerWindowTestCase.DEFAULT_SCREEN
    )
    @patch(
        'wotw_xlib.common.pointer_window.XRootWindow',
        return_value=MagicMock()
    )
    def test_root_discovery(self, mock_root, mock_screen):
        mock_manager = MagicMock()
        mock_manager.attach_mock(mock_root, 'XRootWindow')
        mock_manager.attach_mock(mock_screen, 'XDefaultScreen')
        self.pointer_window.display = self.DEFAULT_DISPLAY
        self.pointer_window.discover_root_window()
        mock_manager.assert_has_calls([
            call.XDefaultScreen(self.DEFAULT_DISPLAY),
            call.XRootWindow(self.DEFAULT_DISPLAY, self.DEFAULT_SCREEN)
        ])


class GetMousePositionUnitTests(PointerWindowTestCase):

    @patch(
        'wotw_xlib.common.pointer_window.XQueryPointer',
        return_value=MagicMock()
    )
    def test_function_call(self, mock_query):
        self.pointer_window.get_mouse_position()
        mock_query.assert_called_once()

    @patch(
        'wotw_xlib.common.pointer_window.XQueryPointer',
        return_value=MagicMock()
    )
    def test_return_points(self, mock_query):
        empty = Point(0, 0)
        root, win = self.pointer_window.get_mouse_position()
        self.assertEquals(empty.x, root.x)
        self.assertEquals(empty.y, root.y)
        self.assertEquals(empty.x, win.x)
        self.assertEquals(empty.y, win.y)
