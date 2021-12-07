from timeInterval import *
from year import *
from season import *

def test_fractions():
    assert timeInterval(1,6) == timeInterval(1.25)
    assert timeInterval(0, 7.5) == timeInterval(0,7,540)
    assert timeInterval(1.1) == timeInterval(1,2,432)
    assert timeInterval(0,0,1) == timeInterval(0,0,1.5)
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
    
# Test values in 6:6
exampleMonth = timeInterval(1,17,107)
def test_adding_tuple():
    assert exampleMonth + (1,12,793) == timeInterval(3,5,900)
def test_BHRD():
    assert BHRD + (4, 8, 876) == timeInterval(6, 14)
