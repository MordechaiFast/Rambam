from calendarUnits import Year, Month, LEAP_YEARS
def test_month_lengths():
    # 8:5
    for month in Year(1):
        if   month.monthCount in {1, 5, 7, 9, 11}:  #Heshvan, (Teves), Addar, Iyyar, Tamuz, Ellul
            assert month.two_day_Rosh_Chodesh()
        elif month.monthCount in {0, 4, 6, 8, 10}:     #Tishrei, (Kislev), Shevat, Nissan, Sivan, Av
            assert not month.two_day_Rosh_Chodesh()

    for month in Year(3):
        if   month.monthCount in {1, 5, 6, 8, 10, 12}:
            assert month.two_day_Rosh_Chodesh()
        elif month.monthCount in {0, 4, 7, 9, 11}:
            assert not month.two_day_Rosh_Chodesh()
def test_variable_months():
    # 8:7
    # To speed things up, calculate once, use twice
    nextYear = Year(1)
    for _ in range(1, 100):
        thisYear = nextYear
        nextYear = thisYear.yearAfter()
        daysBetween = (nextYear.Rosh_Hashana() - thisYear.Rosh_Hashana() - 1) % 7
        if thisYear.placeInCycle not in LEAP_YEARS:
            if   daysBetween == 2:
                assert not Month(thisYear, 9).two_day_Rosh_Chodesh()
                assert not Month(thisYear, 10).two_day_Rosh_Chodesh()
            elif daysBetween == 3:
                assert not Month(thisYear, 9).two_day_Rosh_Chodesh()
                assert Month(thisYear, 10).two_day_Rosh_Chodesh()
            elif daysBetween == 4:
                assert Month(thisYear, 9).two_day_Rosh_Chodesh()
                assert Month(thisYear, 10).two_day_Rosh_Chodesh()
        # 8:8
        else:
            if   daysBetween == 4:
                assert not Month(thisYear, 9).two_day_Rosh_Chodesh()
                assert not Month(thisYear, 10).two_day_Rosh_Chodesh()
            elif daysBetween == 5:
                assert not Month(thisYear, 9).two_day_Rosh_Chodesh()
                assert Month(thisYear, 10).two_day_Rosh_Chodesh()
            elif daysBetween == 6:
                assert Month(thisYear, 9).two_day_Rosh_Chodesh()
                assert Month(thisYear, 10).two_day_Rosh_Chodesh()        
def test_check_rules():
    # 8:9
    for i in range(1, 100):
        thisYear = Year(i)
        if thisYear.Rosh_Hashana() == 3:
            assert not Month(thisYear, 9).two_day_Rosh_Chodesh()
            assert Month(thisYear, 10).two_day_Rosh_Chodesh()
        elif thisYear.Rosh_Hashana() in {7, 2}:
            # This year is not kisidran 
            assert Month(thisYear, 9).two_day_Rosh_Chodesh() \
            or not Month(thisYear, 10).two_day_Rosh_Chodesh() 
        elif thisYear.Rosh_Hashana() == 5:
            if thisYear.placeInCycle not in LEAP_YEARS:
                # Not hasser
                assert Month(thisYear, 10).two_day_Rosh_Chodesh()
            else:
                assert Month(thisYear, 9).two_day_Rosh_Chodesh() \
                or not Month(thisYear, 10).two_day_Rosh_Chodesh() 