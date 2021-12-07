from timeInterval import *
from year import *
from season import *

def test_fractional_day():
    assert timeInterval(1,6) == timeInterval(1.25)
def test_fractional_hours():
    assert timeInterval(0, 7.5) == timeInterval(0,7,540)
def test_hard_fraction():
    assert timeInterval(1.1) == timeInterval(1,2,432)
def test_all_lengths():
    # Test values in 6:4
    assert lunarYear == timeInterval(354, 8, 876)
    assert leapYear == timeInterval(383, 21, 589)
    assert solarYear == timeInterval(365, 6)
    assert solarYearExcess == timeInterval(10, 21, 204)
    # Test values in 6:5
    assert lunarMonthRemainder == timeInterval(1, 12, 793)
    assert lunarYearRemainder ==  timeInterval(4, 8, 876)
    assert leapYearRemainder == timeInterval(5, 21, 589)