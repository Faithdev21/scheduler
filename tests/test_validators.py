import unittest
from scheduler.validators import is_valid_date, is_valid_time


class TestValidators(unittest.TestCase):

    def test_valid_date(self):
        self.assertTrue(is_valid_date("2023-11-01"))

    def test_invalid_date_format(self):
        self.assertFalse(is_valid_date("2023-13-01"))

    def test_valid_time(self):
        self.assertTrue(is_valid_time("12:30"))

    def test_invalid_time(self):
        self.assertFalse(is_valid_time("25:00"))

    def test_invalid_time_string(self):
        self.assertFalse(is_valid_time("abc"))
