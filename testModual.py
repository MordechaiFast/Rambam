import unittest
from timeInterval import *
from year import *
from season import*

class TestLengthValues(unittest.TestCase):

    # Test values in 6:4
    def test_year_length(self):
        self.assertEqual(lunarYear, timeInterval(354, 8, 876))
    def test_leap_year_length(self):
        self.assertEqual(leapYear, timeInterval(383, 21, 589))
    def test_solar_year_length(self):
        self.assertEqual(solarYear, timeInterval(365, 6))
    def test_solar_year_excess(self):
        self.assertEqual(solarYearExcess, timeInterval(10, 21, 204))

if __name__ == '__main__':
    unittest.main()