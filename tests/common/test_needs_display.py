# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

from ctypes import c_char_p
from unittest import TestCase

from mock import patch


from wotw_xlib.common import NeedsDisplay
from wotw_xlib.xlib import Display


class NeedsDisplayTestCase(TestCase):
    DEFAULT_DISPLAY = None
    PARSED_DISPLAY = 'a display'

    def setUp(self):
        self.construct_needs_display()

    def wipe_needs_display(self):
        del self.has_display

    def construct_needs_display(self):
        open_display_patcher = patch.object(NeedsDisplay, 'open_display')
        open_display_patcher.start()
        self.has_display = NeedsDisplay(self.DEFAULT_DISPLAY)
        open_display_patcher.stop()
        self.addCleanup(self.wipe_needs_display)


class ConstructorUnitTests(NeedsDisplayTestCase):

    @patch(
        'wotw_xlib.common.NeedsDisplay.parse_unknown_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_flag_is_set(self, mock_parse):
        has_display = NeedsDisplay(self.DEFAULT_DISPLAY)
        self.assertFalse(has_display.opened_display)

    @patch(
        'wotw_xlib.common.NeedsDisplay.parse_unknown_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_parse_is_called(self, mock_parse):
        NeedsDisplay(self.DEFAULT_DISPLAY)
        mock_parse.assert_called_once_with(self.DEFAULT_DISPLAY)


class ParseUnknownDisplayUnitTests(NeedsDisplayTestCase):

    DISPLAY_INDEX = ':1.0'

    WRONG_INDICES = [47, ['rad', 'stuff'], {'cool': 'beans'}]

    @patch(
        'wotw_xlib.common.NeedsDisplay.open_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_with_a_display(self, mock_open):
        unknown = Display()
        result = self.has_display.parse_unknown_display(unknown)
        self.assertEquals(mock_open.call_count, 0)
        self.assertEquals(unknown, result)

    @patch(
        'wotw_xlib.common.NeedsDisplay.open_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_with_words(self, mock_open):
        for unknown in [self.DISPLAY_INDEX, c_char_p(self.DISPLAY_INDEX)]:
            result = self.has_display.parse_unknown_display(unknown)
            mock_open.assert_called_once_with(unknown)
            self.assertEquals(result, self.PARSED_DISPLAY)
            mock_open.reset_mock()

    @patch(
        'wotw_xlib.common.NeedsDisplay.open_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_with_wrong_indices(self, mock_open):
        for unknown in self.WRONG_INDICES:
            result = self.has_display.parse_unknown_display(unknown)
            mock_open.assert_called_once_with(None)
            self.assertEquals(result, self.PARSED_DISPLAY)
            mock_open.reset_mock()


class OpenDisplayUnitTests(NeedsDisplayTestCase):

    DISPLAY_TO_OPEN = ':47.0'

    @patch(
        'wotw_xlib.needs_display.XOpenDisplay',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_flag_is_set(self, mock_open):
        self.has_display.open_display(self.DISPLAY_TO_OPEN)
        self.assertTrue(self.has_display.opened_display)

    @patch(
        'wotw_xlib.needs_display.XOpenDisplay',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_parse_is_called(self, mock_open):
        self.has_display.open_display(self.DISPLAY_TO_OPEN)
        mock_open.assert_called_once_with(self.DISPLAY_TO_OPEN)
