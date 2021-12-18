from timeMeasures import timeInWeek, timeInterval

# Constants
BHRD = timeInterval(2,5,204)
"""Starting molad"""
LUNAR_MONTH = timeInterval(29,12,793)
"""The length of a month"""
LUNAR_YEAR = LUNAR_MONTH * 12
"""The lenght of a lunar year of 12 months"""
LEAP_YEAR = LUNAR_MONTH * 13
"""The lenght of a leap year of 13 months"""
LUNAR_MONTH_REMAINDER = timeInWeek(LUNAR_MONTH)
"""The ofset of the molad after one month"""
LUNAR_YEAR_REMAINDER = LUNAR_MONTH_REMAINDER * 12
"""The ofset of the molad after one regular year"""
LEAP_YEAR_REMAINDER = LUNAR_MONTH_REMAINDER * 13
"""The ofset of the molad after one leap year"""
CYCLE_YEARS = 19
"""In a cycle of 19 lunar years with 7 leap years, the number of days is the same as 19 solar years"""
CYCLE = LUNAR_YEAR * 12 + LEAP_YEAR * 7
"""The length of a 19 lunar year cycle with 7 leap years"""
CYCLE_REMAINDER = LUNAR_YEAR_REMAINDER * 12 + LEAP_YEAR_REMAINDER * 7
"""The length of a cycle in days of the week."""
LEAP_YEARS = {0, 3, 6, 8, 11, 14, 17, 19}
"""The leap years in a 19 year cycle are years 3, 6, 8, 11, 14, 17, and 19"""
ADU = {1,4,6}
"""The day of Rosh Chodesh Tishrei (Rosh Hashanah) is never set to days 1, 4, or 6, according to the set calandar. """

class Year:
    """Holds the year number from Creation, 
    the cycles past and place in cycle, 
    the date and day of the week of Rosh Hashana, 
    and the list of whole months."""

    # 1) Take the number of years from the year of creation.
    def __init__(self, count: int, startYear = 1) -> None:
        # startYear being 0 means that this is an internal calculation instance of the year class, and we won't want to calculate if its length, only it's Rosh Hashana day, for the needs of the previous year. 
        if startYear in {1,0}:
            self.yearsFromCreation = count
            """The number of years from year 1 = the year of BHRD"""
        
        # If the year count is not from creation, determin the number of years from creation. 
        else:
            self.yearsFromCreation = startYear - 1 + count
            # E.g. if the starting year is 2 (the year of Man's creation) and the year is 1, then it is two years in the count from the creation year.

        # 2) Divide that into cycles. We now know the number of cycles and the year within the current cycle.
    
        # Since we will have to correct for the last year of  the cycle, first determin the year within the cycle.
        self.placeInCycle = self.yearsFromCreation % CYCLE_YEARS
        """The place in the 19 year cycle from 1-19"""
        if self.placeInCycle == 0:
            self.cyclesToYear = self.yearsFromCreation // CYCLE_YEARS - 1
            """The number of whole 19 year cycles before the current year"""
            self.placeInCycle = CYCLE_YEARS
        else:
            self.cyclesToYear = self.yearsFromCreation // CYCLE_YEARS
    
        # 3) Add together the full cycles
        self.molad =  CYCLE_REMAINDER * self.cyclesToYear + BHRD
        """The molad of the begning of this year"""
        
        # 4) Add the regular years and the leap years

        # The given year does not get its length added to the total time. This is accomplished by the for loop itself; the place in cycle is out of the range.
        for y in range(1, self.placeInCycle):
            if y in LEAP_YEARS: self.molad += LEAP_YEAR_REMAINDER
            else:               self.molad += LUNAR_YEAR_REMAINDER
        
        date = BHRD + CYCLE * self.cyclesToYear
        """The date of the molad in days from Shabbos before BHRD"""
        for y in range(1, self.placeInCycle):
            if y in LEAP_YEARS: date += LEAP_YEAR
            else:               date += LUNAR_YEAR
    
        #(Halacha 15 is in the month class)

        # Defining Rosh Hashana of the year
        #7:1
        # When the molad would have it so, Rosh Chodesh is set to the next day.   
        if self.molad.days in ADU:
            self.day = self.molad.days + 1
            """The day of the week of Rosh Hashanah of this year from 1-7"""

        #7:2
        # If the molad is after noon, Rosh Chodesh is set to the next day, if the next day is not 1, 4 or 6.
        elif self.molad.hours >= 18:
            if self.molad.days % 7 + 1 not in ADU:
            # mod needed in case day is 7, to set it to 0
                self.day = self.molad.days + 1
        
        #7:3
        # If the molad is after noon and the next day is 1, 4, or 6, Rosh Chodesh is two days after the molad.
            elif self.molad.days % 7 + 1 in ADU:
                self.day = self.molad.days % 7 + 2

        #7:4 
        # GTRD - If the molad of Tishrei is on a day 3, and the molad is after 9 hours and 204 chalakim, and the year is not a  leap year, Rosh Chodesh is set to day 5, which is two days after the molad. 
        elif (self.molad.days == 3
          and self.molad >= (3, 9, 204)
          and self.placeInCycle not in LEAP_YEARS):
            self.day = self.molad.days + 2

        #7:5 
        # BTU TKPT - If the molad of Tishrei is on a day 2, and the molad is after 15 hours and 589 chalakim, and it is the year after a  leap year, Rosh Chodesh is set to day 3. 
        elif (self.molad.days == 2
          and self.molad >= (2, 15, 589)
          and self.placeInCycle - 1 in LEAP_YEARS):
            self.day = self.molad.days + 1
        
        #7:6
        # If none of the cases applies, Rosh Hashana is on the day of the molad. 
        else:
            self.day = self.molad.days
        
        if self.day == 7 and self.molad.days == 7:
            # date.days%7==0 so day-days==7, but we want 0
            self.date = date.days
            """The date of Rosh Hashanah of this year in days from Shabbos before BHRD"""
        else:
            self.date = date.days + (self.day - date.days % 7)
        #self.molad.days and date.days%7 were the same before the pushing-off
        
        #8:3 
        # If the length of a month was exactly 29.5 days, the months would go one whole and one short.
        self.wholeMonths = [True, False] * 6
        """Those months that are whole in this year. True = whole"""
        # (This list of whole months starts with Tishrei, and assumes that Marheshvan will be lacking and Kislev will be full.)
        # Since the length of a lunar month is not exactly 29 1/2 days, some years have more whole months than short months and (as a result of pushing off Rosh Hashana) some years have more short months than whole months.
        
        #8:5
        # The months that are always set by the fixed calandar are Nissan 30, Iyyar 29, Sivan 30, Tamuz 29, Av 30, Elul 29, Tishrei 30, Teves 29, Shevat 30, Addar (II) 29. In a leap year Addar I is a full month.
        if self.placeInCycle in LEAP_YEARS: self.wholeMonths.insert(5, True)
        
        #8:6
        yearType = {'full' : False, 'lacking' : False, 'orderly' : False}
        """An indicator if the current year's months (Marhesvan and Kislev) are lacking, whole, or accorting to thier normal pattern, Marheshvan lacking and Kislev whole."""
        
        #8:7
        # Determinimg the type of year for setting the days of Rosh Chodesh of the different months.
        if startYear != 0:
            daysBetween = (self.yearAfter(dummyYear= True).day - self.day - 1) % 7
            """The number of days between Rosh Hashanah this year and Rosh Hashana next year, not inclusive"""
            if self.placeInCycle not in LEAP_YEARS:
                #For different days between, set different year types
                yearType[{2: 'lacking', 3: 'orderly', 4: 'full'}[daysBetween]] = True
            
            #8:8
            else:   #On a leap year:
                yearType[{4: 'lacking', 5: 'orderly', 6: 'full'}[daysBetween]] = True
            
            # (8:6) The months of Marheshvan and Kislev are variable.
            # Tishrei is month 0 
            if yearType['lacking']: self.wholeMonths[2] = False
            if yearType['full']: self.wholeMonths[1] = True
    
    def yearAfter (self, dummyYear = False):
        """Generates the next year after this one.
        
        A dummy year is one that does not determin if its months are lacking or whole."""
        return Year(self.yearsFromCreation + 1, 0 if dummyYear else 1)

MONTH_NAMES = ["Tishrei", "Marchesvan", "Kislev ", "Teves  ", "Shevat ", "Addar  ",
"Nissan ", "Iyyar  ", "Sivan  ", "Tamuz  ", "Av     ", "Elul   "]
MONTH_NAMES_IN_LEAP_YEAR = ["Tishrei", "Marchesvan", "Kislev ", "Teves  ", "Shevat ",
"Addar I", "Addar II", "Nissan ", "Iyyar  ", "Sivan  ", "Tamuz  ", "Av     ", "Elul   "]
#8:1-2 
# A month can only be of whole days.
SHORT_MONTH, WHOLE_MONTH = 29, 30

class Month:
    """monthReference starts with 0 for Tishrei or 1 for Nissan.

    Holds the year that the month is in, 
    the month's name, 
    the molad of that month, 
    and the date and day of the week Rosh Chodesh."""
    
    def __init__(self, year: Year, monthReference: int, startFromTishrei = False) -> None:
        # Save the year
        self.year = year
        """The year that this month is a part of"""

        # Convert month from Nissan to months from Tishrei, when neccesary
        if startFromTishrei:
            monthCount = monthReference
            """The number of this month from Tishrei = 0"""
        else:
            # For months between Tishrei and Nissan: 
            if monthReference > 6:
                # We want Tishrei to be 0, so take away 7.
                monthCount = monthReference - 7
            # For months between Nissan and Tishrei, it depends if the given year is a leap year.
            elif year.placeInCycle in LEAP_YEARS:
                # Nissan is 7 months from Tishrei in a leap year.
                monthCount = monthReference + 6
            else:
                # Nissan is 6 months from Tishrei in a regular year.
                monthCount = monthReference + 5

        # Find the month's name
        if year.placeInCycle not in LEAP_YEARS:
            self.name = MONTH_NAMES[monthCount]
            """The name of the month"""
        else:
            self.name = MONTH_NAMES_IN_LEAP_YEAR[monthCount]
    
        #6:15
        # To find the molad of a specific month, add the molad of a month for each month until the requiered month.
        self.molad = year.molad + LUNAR_MONTH_REMAINDER * monthCount
        """The molad of this month"""

        # Defning the day of Rosh Chodesh
        #8:4
        # For a month following a full month, Rosh Chodesh is two days.
        if year.wholeMonths[monthCount-1]:
        # [-1] returns the last item in the list, which is what we want.
            self.twoDayRoshChodesh = True
            """If this month has a two day Rosh Chodesh"""
        else:
            self.twoDayRoshChodesh = False

        # Working out the date of Rosh Chodesh for the month, and the day of the week. (Not worked out in Rambam.)
        # Start with the first month: Rosh Chodesh Tishrei is Rosh Hashana. 
        self.date = year.date
        """The date of Rosh Chodesh of this month, in days from 
        the Shabbos before BHRD"""

        for i in range (monthCount):
            if year.wholeMonths[i]:
                self.date += WHOLE_MONTH
            else:
                self.date += SHORT_MONTH
        self.day = self.date % 7
        """The day of the week of Rosh Chodesh of this month from 1-7"""
        if self.day == 0: self.day = 7