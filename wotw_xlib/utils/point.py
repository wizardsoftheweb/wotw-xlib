# pylint:disable=invalid-name
"""This file provides the Point util class"""


class Point(object):
    """This class holds very simple Point class with some logic for X11 tasks"""

    def __init__(self, x, y):
        """Simple ctor; assigns sanitized values"""
        self.x = self.parse_coordinate(x)
        self.y = self.parse_coordinate(y)

    @staticmethod
    def parse_coordinate(raw_coordinate):
        """
        Takes a simple number or a ctype number and returns the actual value
        """
        return (
            raw_coordinate.value
            if hasattr(raw_coordinate, 'value')
            else raw_coordinate
        )

    def is_above_and_left_of(self, unknown_point):
        """Checks if this Point is northwest of the unknown point"""
        return (
            self.x <= unknown_point.x
            and
            self.y <= unknown_point.y
        )

    def __str__(self):
        """Prettified Cartesian output"""
        return "(%d,%d)" % (self.x, self.y)
