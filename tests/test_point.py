# pylint: disable=missing-docstring,unused-argument,invalid-name
from __future__ import print_function

from ctypes import c_int
from unittest import TestCase

from mock import patch


from wotw_xlib.utils import Point


class PointTestCase(TestCase):
    NUMBER_OF_COORDINATES_IN_POINT = 2
    DEFAULT_COORDINATE = 47


class ConstructorUnitTests(PointTestCase):

    INPUT_COORDINATE = PointTestCase.DEFAULT_COORDINATE - 10

    @patch(
        'wotw_xlib.Point.parse_coordinate',
        return_value=PointTestCase.DEFAULT_COORDINATE
    )
    def test_parameters_assigned(self, mock_parse):
        sample = Point(self.INPUT_COORDINATE, self.INPUT_COORDINATE)
        self.assertEquals(self.DEFAULT_COORDINATE, sample.x)
        self.assertEquals(self.DEFAULT_COORDINATE, sample.y)

    @patch(
        'wotw_xlib.Point.parse_coordinate',
        return_value=PointTestCase.DEFAULT_COORDINATE
    )
    def test_parse_call_count(self, mock_parse):
        Point(self.INPUT_COORDINATE, self.INPUT_COORDINATE)
        self.assertEquals(
            self.NUMBER_OF_COORDINATES_IN_POINT,
            mock_parse.call_count
        )


class ParseCoordinatesUnitTests(PointTestCase):

    def test_plain_number(self):
        output = Point.parse_coordinate(self.DEFAULT_COORDINATE)
        self.assertEquals(self.DEFAULT_COORDINATE, output)

    def test_ctype_number(self):
        ctype_coord = c_int(self.DEFAULT_COORDINATE)
        self.assertNotEquals(ctype_coord, self.DEFAULT_COORDINATE)
        output = Point.parse_coordinate(ctype_coord)
        self.assertEquals(self.DEFAULT_COORDINATE, output)


class IsAboveAndLeftOfUnitTests(PointTestCase):

    def test_cardinal_directions(self):
        origin = Point(0, 0)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                print(x, y)
                self.assertEquals(
                    origin.is_above_and_left_of(Point(x, y)),
                    x > -1 and y > -1
                )
