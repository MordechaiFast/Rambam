import unittest
from timeInterval import *
from year import *
from season import*

class TestLengthValues(unittest.TestCase):

    # Test values in 6:4
    def test_year_length(self):
        self.assertEqual(LUNAR_YEAR, timeInterval(354, 8, 876))
    def test_leap_year_length(self):
        self.assertEqual(LEAP_YEAR, timeInterval(383, 21, 589))
    def test_solar_year_length(self):
        self.assertEqual(solarYear, timeInterval(365, 6))
    def test_solar_year_excess(self):
        self.assertEqual(solarYearExcess, timeInterval(10, 21, 204))

    # Test values in 6:5
    def test_month_molad(self):
        self.assertEqual(LUNAR_MONTH_REMAINDER, timeInterval(1, 12, 793))
    def test_year_molad(self):
        self.assertEqual(LUNAR_YEAR_REMAINDER, timeInterval(4, 8, 876))
    def test_leap_lear_molad(self):
        self.assertEqual(LEAP_YEAR_REMAINDER, timeInterval(5, 21, 589))

    # Test non-intiger values
    def test_fractional_days(self):
        self.assertEqual(timeInterval(1,6), timeInterval(1.25))
    def test_fractional_hours(self):
        self.assertEqual(timeInterval(0, 7.5), timeInterval(0,7,540))
  
    
    #def test_cycle_molad(self):
        #self.assertEqual(cycleRemainder, timeInterval())

if __name__ == '__main__':
    unittest.main()