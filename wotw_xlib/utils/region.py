# pylint:disable=invalid-name,too-few-public-methods
"""This file provides the Region util class"""

from wotw_xlib.utils import Point


class Region(object):
    """This class simplifies window geometry using the Point class"""

    def __init__(self, top_left, width=0, height=0):
        """Ctor assigns the two bounding corners"""
        self.top_left = top_left
        self.bottom_right = Point(
            self.top_left.x + Point.parse_coordinate(width),
            self.top_left.y + Point.parse_coordinate(height)
        )

    def contains(self, unknown_point):
        """Test if the region contains an unknown point"""
        return (
            self.top_left.is_above_and_left_of(unknown_point)
            and
            unknown_point.is_above_and_left_of(self.bottom_right)
        )

    def __str__(self):
        """Prettified Cartesian (sorta) output"""
        return "%sx%s" % (self.top_left, self.bottom_right)
