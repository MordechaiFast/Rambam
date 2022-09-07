from classes.calendarUnits import *
from classes.season import *

def test_lengths():
    # Test values in 6:2
    # HOURS_IN_DAY == 24
    # CHALAKIM_IN_HOUR == 1080
    # 6:3
    # Equivilance test
    assert LUNAR_MONTH == (29, 12, 793)
def test_math():
    # 6:4
    # Multiplication test
    assert LUNAR_YEAR == (354, 8, 876)
    assert LEAP_YEAR == (383, 21, 589)
    # Two place tI test
    assert SOLAR_YEAR == (365, 6)
    # Subtraction test
    assert SOLAR_YEAR_EXCESS == (10, 21, 204)
def test_remainders():
    #6:5
    # Tests with rounding days to weeks
    assert LUNAR_MONTH_REMAINDER == (1, 12, 793)
    assert LUNAR_YEAR_REMAINDER ==  (4, 8, 876)
    assert LEAP_YEAR_REMAINDER == (5, 21, 589)
def test_adding():
    # 6:6-7
    exampleMonth = TimeInterval(1,17,107)
    assert exampleMonth + (1,12,793) == (3,5,900)    
def test_BHRD():
    # 6:8
    assert BHRD == (2, 5, 204)
def test_rounding():
    # 6:9
    # Rounding test
    assert BHRD + LUNAR_YEAR == (6, 14)
def test_cycle():
    # 6:10
    # Combined arithmatic test
    assert SOLAR_CYCLE_EXCESS == (0, 1, 485)
    # 6:11
    assert LEAP_YEARS >= {3, 6, 8, 11, 14, 17, 19}
    # For internal reasons, leapYears includes 0.
    # 6:12
    assert CYCLE_REMAINDER == (2, 16, 595)
    # 6:13
    assert CYCLE_REMAINDER + BHRD == (4, 21, 799)
def test_year():
    assert Year(20).molad == (4, 21, 799)
    # 6:14
    assert Year(21).molad == (2, 6, 595)
def test_month():
    # 6:15
    assert Month(Year(21), 7).molad == (2, 6, 595)
    assert Month(Year(21), 0, start_from_Tishrei= True).molad == (2, 6, 595)
    assert Month(Year(21), 8).molad == (3, 19, 308)
    # Calculate Nissan
    assert Month(Year(21), 1, start_from_Tishrei= False).molad == (4, 10, 1033)
    # Nissan in a leap year
    assert Month(Year(22), 1, start_from_Tishrei= False).molad == (3, 8, 542)