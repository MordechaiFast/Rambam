from timeInterval import CHALAKIM_IN_HOUR, HOURS_IN_DAY
from year import *
from season import *

def test_lengths():
    # Test values in 6:2
    # Number of hours in day and chalakim in hours
    assert HOURS_IN_DAY == 24
    assert CHALAKIM_IN_HOUR == 1080
    # 6:3
    assert lunarMonth == (29, 12, 793)
def test_math():
    # 6:4
    # Multiplication test
    assert lunarYear == (354, 8, 876)
    # Addition test
    assert leapYear == (383, 21, 589)
    # Equivilance test
    assert solarYear == (365, 6)
    # Subtraction test
    assert solarYearExcess == (10, 21, 204)
def test_remainders():
    #6:5
    # Tests with rounding days to weeks
    assert lunarMonthRemainder == (1, 12, 793)
    assert lunarYearRemainder ==  (4, 8, 876)
    assert leapYearRemainder == (5, 21, 589)
    # Test value in 9:1
    assert seasonLength == (91,7.5)
def test_adding():
    # Test values in 6:6-7
    exampleMonth = timeInterval(1,17,107)
    assert exampleMonth + (1,12,793) == (3,5,900)    
def test_BHRD():
    # Test of 6:8
    # Rambam doesn't say this explicitly, but this is where BHRD comes from.
    assert BHRD + (4, 8, 876) == (6, 14)
def test_rounding():
    # Test of 6:9
    assert timeInWeek(BHRD) + (5,18,876) == timeInWeek(timeInterval(1))
def test_cycle():
    # Test of 6:10
    assert solarCycleExcess == (0, 1, 485)
    # Test of 6:11
    assert {3,6,8,11,14,17,19} <= leapYears
    # For internal reasons, leapYears includes 0.
    # 6:12
    assert cycleRemainder == (2, 16, 595)