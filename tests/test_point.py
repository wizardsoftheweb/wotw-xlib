# pylint: disable=missing-docstring,unused-argument
from unittest import TestCase

from mock import patch

from wotw_xlib.utils import Point


class ConstructorUnitTests(TestCase):

    NUMBER_OF_COORDINATES_IN_POINT = 2
    DEFAULT_COORDINATE = 47
    INPUT_COORDINATE = DEFAULT_COORDINATE - 10

    @patch(
        'wotw_xlib.Point.parse_coordinate',
        return_value=DEFAULT_COORDINATE
    )
    def test_parameters_assigned(self, mock_parse):
        sample = Point(self.INPUT_COORDINATE, self.INPUT_COORDINATE)
        self.assertEquals(self.DEFAULT_COORDINATE, sample.x)
        self.assertEquals(self.DEFAULT_COORDINATE, sample.y)

    @patch(
        'wotw_xlib.Point.parse_coordinate',
        return_value=DEFAULT_COORDINATE
    )
    def test_parse_call_count(self, mock_parse):
        Point(self.INPUT_COORDINATE, self.INPUT_COORDINATE)
        self.assertEquals(
            self.NUMBER_OF_COORDINATES_IN_POINT,
            mock_parse.call_count
        )
