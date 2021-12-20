from calendarUnits import Year, Month, LEAP_YEARS
def test_month_lengths():
    # 8:5
    thisYear = Year(1)
    for i in range(1, 13):
        thisMonth = Month(thisYear, i)
        if   i in {1, 3, 5, 7, 11}:
            assert not thisMonth.twoDayRoshChodesh
        elif i in {2, 4, 6, 8, 12}:
            assert thisMonth.twoDayRoshChodesh

    thisYear = Year(3)
    for i in range(1, 14):
        thisMonth = Month(thisYear, i)
        if   i in {1, 3, 5, 7, 11}:
            assert not thisMonth.twoDayRoshChodesh
        elif i in {2, 4, 6, 8, 12, 13}:
            assert thisMonth.twoDayRoshChodesh
def test_variable_months():
    # 8:7
    # To speed things up, calculate once, use twice
    nextYear = Year(1)
    for i in range(1, 100):
        thisYear = nextYear
        nextYear = thisYear.yearAfter()
        daysBetween = (nextYear.day - thisYear.day - 1) % 7
        if thisYear.placeInCycle not in LEAP_YEARS:
            if   daysBetween == 2:
                assert not Month(thisYear, 9).twoDayRoshChodesh
                assert not Month(thisYear, 10).twoDayRoshChodesh
            elif daysBetween == 3:
                assert not Month(thisYear, 9).twoDayRoshChodesh
                assert Month(thisYear, 10).twoDayRoshChodesh
            elif daysBetween == 4:
                assert Month(thisYear, 9).twoDayRoshChodesh
                assert Month(thisYear, 10).twoDayRoshChodesh
        # 8:8
        else:
            if   daysBetween == 4:
                assert not Month(thisYear, 9).twoDayRoshChodesh
                assert not Month(thisYear, 10).twoDayRoshChodesh
            elif daysBetween == 5:
                assert not Month(thisYear, 9).twoDayRoshChodesh
                assert Month(thisYear, 10).twoDayRoshChodesh
            elif daysBetween == 6:
                assert Month(thisYear, 9).twoDayRoshChodesh
                assert Month(thisYear, 10).twoDayRoshChodesh            
def test_check_rules():
    # 8:9
    for i in range(1, 100):
        thisYear = Year(i)
        if thisYear.day == 3:
            assert not Month(thisYear, 9).twoDayRoshChodesh
            assert Month(thisYear, 10).twoDayRoshChodesh
        elif thisYear.day in {7, 2}:
            # This year is not kisidran 
            assert Month(thisYear, 9).twoDayRoshChodesh or not Month(thisYear, 10).twoDayRoshChodesh 
        elif thisYear.day == 5:
            if thisYear.placeInCycle not in LEAP_YEARS:
                # Not hasser
                assert Month(thisYear, 10).twoDayRoshChodesh
            else:
                assert Month(thisYear, 9).twoDayRoshChodesh or not Month(thisYear, 10).twoDayRoshChodesh 