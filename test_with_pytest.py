from timeInterval import *
from year import *
from season import *

def test_fractions():
    assert timeInterval(1.25) == timeInterval(1,6)
    assert timeInterval(0, 7.5) == timeInterval(0,7,540)
    assert timeInterval(1.1) == timeInterval(1,2,432)
    assert timeInterval(0,0,1.5) == timeInterval(0,0,1)
def test_all_lengths():
    # Test values in 6:4
    # Multiplication test
    assert lunarYear == timeInterval(354, 8, 876)
    # Addition test
    assert leapYear == timeInterval(383, 21, 589)
    # Equivilance test
    assert solarYear == timeInterval(365, 6)
    # Subtraction test
    assert solarYearExcess == timeInterval(10, 21, 204)
    # Test values in 6:5
    # Tests with rounding days to weeks
    assert lunarMonthRemainder == timeInterval(1, 12, 793)
    assert lunarYearRemainder ==  timeInterval(4, 8, 876)
    assert leapYearRemainder == timeInterval(5, 21, 589)
    
# Test values in 6:6-7
exampleMonth = timeInterval(1,17,107)
def test_adding_tuple():
    assert exampleMonth + (1,12,793) == timeInterval(3,5,900)
    assert exampleMonth + (1,12) == timeInterval(3,5,107)
# Test of 6:8
def test_BHRD():
    assert BHRD + (4, 8, 876) == timeInterval(6, 14)
# Test of 6:9
def test_rounding():
    assert timeInWeek(BHRD) + (5,18,876) == timeInWeek(timeInterval(1))

# Try negitave time
def test_add_negetive():
    assert BHRD + (-1, -2, -4) == timeInterval(1, 3, 200)
def test_subtract_negetive():
    assert BHRD - (-1, -2, -4) == timeInterval(3, 7, 208)
def test_negetive_result():
    assert BHRD - (7,) == timeInterval(-5, 5, 204)
    assert BHRD - (7, 5, 204) == timeInterval(-5)
    assert BHRD - (7, 6) == timeInterval(-6, 23, 204)