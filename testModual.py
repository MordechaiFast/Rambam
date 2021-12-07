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

    # Test values in 6:5
    def test_month_molad(self):
        self.assertEqual(lunarMonthRemainder, timeInterval(1, 12, 793))
    def test_year_molad(self):
        self.assertEqual(lunarYearRemainder, timeInterval(4, 8, 876))
    def test_leap_lear_molad(self):
        self.assertEqual(leapYearRemainder, timeInterval(5, 21, 589))
    
    #def test_cycle_molad(self):
        #self.assertEqual(cycleRemainder, timeInterval())

if __name__ == '__main__':
    unittest.main()