# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

from unittest import TestCase

from mock import patch


from wotw_xlib.common import NeedsDisplay


class NeedsDisplayTestCase(TestCase):
    DEFAULT_DISPLAY = None
    PARSED_DISPLAY = 'a display'


class ConstructorUnitTests(NeedsDisplayTestCase):

    @patch(
        'wotw_xlib.common.NeedsDisplay.parse_unknown_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_flag_is_set(self, mock_parse):
        display = NeedsDisplay(self.DEFAULT_DISPLAY)
        self.assertFalse(display.opened_display)

    @patch(
        'wotw_xlib.common.NeedsDisplay.parse_unknown_display',
        return_value=NeedsDisplayTestCase.PARSED_DISPLAY
    )
    def test_parse_is_called(self, mock_parse):
        NeedsDisplay(self.DEFAULT_DISPLAY)
        mock_parse.assert_called_once_with(self.DEFAULT_DISPLAY)
