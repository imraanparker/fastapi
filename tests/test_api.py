# -*- coding: utf-8 -*-
import unittest
from app.main import calculate_business_hours


class TestAPI(unittest.TestCase):

    def test_one_jan(self):
        v = calculate_business_hours("2020-01-01", "2020-01-03")
        self.assertEqual(v.body, b"64800")

    def test_start_time_fail(self):
        v = calculate_business_hours("2020-01-01T", "2020-01-03")
        self.assertIn(b"Start time invalid:", v.body)

    def test_end_time_fail(self):
        v = calculate_business_hours("2020-01-01", "2020-01-03T")
        self.assertIn(b"End time invalid:", v.body)

    def test_large_difference(self):
        v = calculate_business_hours("2000-01-01", "2030-12-31")
        self.assertEqual(v.body, b"251553600")

if __name__ == "__main__":
    unittest.main(verbosity=2)