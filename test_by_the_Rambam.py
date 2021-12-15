from timeInterval import CHALAKIM_IN_HOUR, HOURS_IN_DAY
from year import *
from season import *

def test_lengths():
    # Test values in 6:2
    assert HOURS_IN_DAY == 24
    assert CHALAKIM_IN_HOUR == 1080
    # 6:3
    # Equivilance test
    assert lunarMonth == (29, 12, 793)
def test_math():
    # 6:4
    # Multiplication test
    assert lunarYear == (354, 8, 876)
    # Addition test
    assert leapYear == (383, 21, 589)
    # Two place tI test
    assert solarYear == (365, 6)
    # Subtraction test
    assert solarYearExcess == (10, 21, 204)
def test_remainders():
    #6:5
    # Tests with rounding days to weeks
    assert lunarMonthRemainder == (1, 12, 793)
    assert lunarYearRemainder ==  (4, 8, 876)
    assert leapYearRemainder == (5, 21, 589)
def test_adding():
    # 6:6-7
    exampleMonth = timeInterval(1,17,107)
    assert exampleMonth + (1,12,793) == (3,5,900)    
def test_BHRD():
    # 6:8
    # Rambam doesn't say this explicitly, but this is where BHRD comes from.
    assert BHRD + (4, 8, 876) == (6, 14)
def test_rounding():
    # 6:9
    # Rounding test
    assert timeInWeek(BHRD) + (5,18,876) == timeInWeek(timeInterval(1))
def test_cycle():
    # Test of 6:10
    # Combined arithmatic test
    assert solarCycleExcess == (0, 1, 485)
    # Test of 6:11
    assert leapYears >= {3, 6, 8, 11, 14, 17, 19}
    # For internal reasons, leapYears includes 0.
    # 6:12
    assert cycleRemainder == (2, 16, 595)
    # 6:13
    assert cycleRemainder + BHRD == (4, 21, 799)
def test_year():
    assert year(20).molad == (4, 21, 799)
    # 6:14
    assert year(21).molad == (2, 6, 595)
def test_month():
    # 6:15
    assert month(year(21), 8).molad == (3, 19, 308)

def test_lo_ADU_rosh():
    # 7:1
    print("7:1")
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 1: break
    assert thisYear.day == 2
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")
    
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 4: break
    assert thisYear.day == 5    
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")
    
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 6: break
    assert thisYear.day == 7        
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

def test_molad_zakan():
    #7:2-3
    print("7:2")
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 2 and thisYear.molad.hours >= 18: break
    assert thisYear.day == 3
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")
    
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 2 and thisYear.molad.hours < 18: break
    assert thisYear.day == 2
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

    print("7:3")
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 7 and thisYear.molad.hours >= 18: break
    assert thisYear.day == 2
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 3 and thisYear.molad.hours >= 18: break
    assert thisYear.day == 5
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 5 and thisYear.molad.hours >= 18: break
    assert thisYear.day == 7
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

def test_GTRD():
    #7:4
    print("7:4")
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 3 and thisYear.molad >= (3, 9, 204) and thisYear.placeInCycle not in leapYears: break
    assert thisYear.day == 5
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

def test_BTUTKPT():
    #7:5
    print("7:5")
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 2 and thisYear.molad >= (2, 15, 589) and thisYear.placeInCycle -1 in leapYears: break
    assert thisYear.day == 3
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

def test_not_GTRD():
    # 7:6
    print("7:6")
    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 3 and thisYear.molad < (3, 9, 204) and thisYear.placeInCycle not in leapYears: break
    assert thisYear.day == 3
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")

    for i in range(1, 6000):
        thisYear = year(i)
        if thisYear.molad.days == 2 and thisYear.molad < (2, 15, 589) and thisYear.placeInCycle - 1 in leapYears: break
    assert thisYear.day == 2
    print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.day}")
    

def test_season():
    # 9:1
    # Floor division test
    assert seasonLength == (91,7.5)
