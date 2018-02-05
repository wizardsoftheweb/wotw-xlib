# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

# from ctypes import c_char_p
from unittest import TestCase

from mock import MagicMock, patch


from wotw_xlib.common import PointerWindow
# from wotw_xlib.xlib import Display


class PointerWindowTestCase(TestCase):
    DEFAULT_DISPLAY = None
    PARSED_DISPLAY = 'a display'
    DEFAULT_WINDOW_ID = 47

    def setUp(self):
        self.construct_pointer_window()

    def wipe_pointer_window(self):
        del self.window

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
        self.window = PointerWindow(
            self.DEFAULT_DISPLAY,
            self.DEFAULT_WINDOW_ID
        )
        self.addCleanup(parse_window_id_patcher.stop)
        self.addCleanup(get_region_patcher.stop)
        self.addCleanup(super_patcher.stop)
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
        self.assertIsNone(self.window.window_attributes)
