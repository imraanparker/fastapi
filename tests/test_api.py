# -*- coding: utf-8 -*-
import unittest
from app.main import calculate_business_hours
from app import utils


class TestAPI(unittest.TestCase):

    def test_one_jan(self):
        # 1 Jan is a holiday so only two days are counted
        v = calculate_business_hours("2020-01-01", "2020-01-03")
        self.assertEqual(v.body, b"64800")

    def test_start_time_fail(self):
        # Invalid start date
        v = calculate_business_hours("2020-01-01T", "2020-01-03")
        self.assertIn(b"Start time invalid:", v.body)

    def test_end_time_fail(self):
        # Invalid end date
        v = calculate_business_hours("2020-01-01", "3099-01-03T")
        self.assertIn(b"End time invalid:", v.body)

    def test_min_start_year(self):
        # The min start year
        year = utils.START_YEAR - 1
        v = calculate_business_hours("%s-01-01" % year, "2020-01-03")
        self.assertIn(b"The date range must be between the years", v.body)

    def test_max_end_year(self):
        # The max end year
        year = utils.END_YEAR
        v = calculate_business_hours("2020-01-01", "%s-01-03" % year)
        self.assertIn(b"The date range must be between the years", v.body)

    def test_large_range(self):
        # Large range
        v = calculate_business_hours("1582-01-01", "3099-12-31")
        self.assertEqual(v.body, b"12318739200")

    def test_easter(self):
        # Make sure easter does not count
        v = calculate_business_hours("2020-04-10", "2020-04-13")
        self.assertEqual(v.body, b"0")

    def test_holiday_on_sunday(self):
        # Make sure the Monday after a public holiday is not counted. 9 Aug 2020 lands on a Sunday
        v = calculate_business_hours("2020-08-08", "2020-08-10")
        self.assertEqual(v.body, b"0")

if __name__ == "__main__":
    unittest.main(verbosity=2)
