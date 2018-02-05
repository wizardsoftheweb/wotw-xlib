# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

from ctypes import c_int
from unittest import TestCase

from mock import patch


from wotw_xlib.utils import Point, Region


class RegionTestCase(TestCase):
    NUMBER_OF_COORDINATES_IN_POINT = 2
    DEFAULT_TOP_LEFT = Point(0, 0)
    DEFAULT_WIDTH = 2
    DEFAULT_HEIGHT = 2
    DEFAULT_BOTTOM_RIGHT = Point(2, 2)


class ConstructorUnitTests(RegionTestCase):

    @patch(
        'wotw_xlib.Point.parse_coordinate',
        return_value=0
    )
    def test_assignment(self, mock_parse):
        region = Region(
            self.DEFAULT_TOP_LEFT,
            self.DEFAULT_WIDTH,
            self.DEFAULT_HEIGHT
        )
        self.assertEquals(region.top_left.x, region.bottom_right.x)
        self.assertEquals(region.top_left.y, region.bottom_right.y)


class StrUnitTests(RegionTestCase):

    def test_to_string(self):
        region = Region(
            self.DEFAULT_TOP_LEFT,
            self.DEFAULT_WIDTH,
            self.DEFAULT_HEIGHT
        )
        self.assertEquals(
            region.__str__(),
            '(0,0)x(2,2)'
        )
