from __future__ import print_function

from unittest import TestCase

# from mock import call, MagicMock, patch


class SampleTests(TestCase):
    DEFAULT_VALUE = 6

    def test_something(self):
        self.assertEquals(self.DEFAULT_VALUE, 8 - 2)
