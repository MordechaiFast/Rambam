from classes.calendarUnits import *
def test_GTRD_and_BTUTKPT():
    assert GTRD == (3, 9, 204)
    assert BTU_TKPT == (2, 15, 589)
def test_all_dechios():
    wantedYears = [None] * 15
    for i in range(1, 100):
        thisYear = Year(i)
        # 7:1
        if   thisYear.molad.days == 1:
            assert thisYear.Rosh_Hashana == 2
            if not wantedYears[0]:
                wantedYears[0] = thisYear
        elif thisYear.molad.days == 4:
            assert thisYear.Rosh_Hashana == 5
            if not wantedYears[1]:
                wantedYears[1] = thisYear
        elif thisYear.molad.days == 6:
            assert thisYear.Rosh_Hashana == 7
            if not wantedYears[2]:
                wantedYears[2] = thisYear
        # 7:2
        elif(thisYear.molad.days == 2 
         and thisYear.molad.hours >= 18):
            assert thisYear.Rosh_Hashana == 3
            if not wantedYears[3]:
                wantedYears[3] = thisYear
        elif(thisYear.molad.days == 2
         and thisYear.molad.hours < 18 
         and thisYear.place_in_cycle -1 not in LEAP_YEARS):
            assert thisYear.Rosh_Hashana == 2
            if not wantedYears[4]:
                wantedYears[4] = thisYear
        # 7:3
        elif thisYear.molad.days == 7 and thisYear.molad.hours >= 18:
            assert thisYear.Rosh_Hashana == 2
            if not wantedYears[5]:
                wantedYears[5] = thisYear
        elif thisYear.molad.days == 3 and thisYear.molad.hours >= 18:
            assert thisYear.Rosh_Hashana == 5
            if not wantedYears[6]:
                wantedYears[6] = thisYear
        elif thisYear.molad.days == 5 and thisYear.molad.hours >= 18:
            assert thisYear.Rosh_Hashana == 7
            if not wantedYears[7]:
                wantedYears[7] = thisYear
        # 7:4
        elif(thisYear.molad.days == 3
         and thisYear.molad >= (3, 9, 204)
         and thisYear.place_in_cycle not in LEAP_YEARS):
            assert thisYear.Rosh_Hashana == 5
            if not wantedYears[8]:
                wantedYears[8] = thisYear
        # 7:5
        elif(thisYear.molad.days == 2
         and thisYear.molad >= (2, 15, 589)
         and thisYear.place_in_cycle -1 in LEAP_YEARS):
            assert thisYear.Rosh_Hashana == 3
            if not wantedYears[9]:
                wantedYears[9] = thisYear
        # 7:6
        elif(thisYear.molad.days == 3
         and thisYear.molad < (3, 9, 204)
         and thisYear.place_in_cycle not in LEAP_YEARS):
            assert thisYear.Rosh_Hashana == 3
            if not wantedYears[10]:
                wantedYears[10] = thisYear
        elif(thisYear.molad.days == 2
         and thisYear.molad < (2, 15, 589)
         and thisYear.place_in_cycle - 1 in LEAP_YEARS):
            assert thisYear.Rosh_Hashana == 2
            if not wantedYears[11]:
                wantedYears[11] = thisYear
        # More cases where the day of Rosh Hashanah is the day of the molad
        elif(thisYear.molad.days == 3
         and thisYear.molad.hours < 18
         and thisYear.place_in_cycle in LEAP_YEARS):
            assert thisYear.Rosh_Hashana == 3
            if not wantedYears[12]:
                wantedYears[12] = thisYear
        elif thisYear.molad.days == 5 and thisYear.molad.hours < 18:
            assert thisYear.Rosh_Hashana == 5
            if not wantedYears[13]:
                wantedYears[13] = thisYear
        elif thisYear.molad.days == 7 and thisYear.molad.hours < 18:
            assert thisYear.Rosh_Hashana == 7
            if not wantedYears[14]:
                wantedYears[14] = thisYear
    print()
    for thisYear in wantedYears:
        print (f"Year {thisYear.yearsFromCreation:>2} Molad {thisYear.molad} Rosh Hashana {thisYear.Rosh_Hashana}")