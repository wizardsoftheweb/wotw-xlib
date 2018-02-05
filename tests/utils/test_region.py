# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

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


class ContainsUnitTests(RegionTestCase):

    def test_contains(self):
        region = Region(
            self.DEFAULT_TOP_LEFT,
            self.DEFAULT_WIDTH,
            self.DEFAULT_HEIGHT
        )
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                print(x, y)
                self.assertEquals(
                    region.contains(Point(x, y)),
                    x > -1 and y > -1
                )


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
