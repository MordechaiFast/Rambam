# This class needs cycle, cycleYears, and BHRD.
from timeInterval import timeInterval

BHRD = timeInterval(2,5,204)
"""Starting molad"""
lunarMonth = timeInterval(29,12,793)
"""The length of a month"""
lunarYear = lunarMonth * 12
"""The lenght of a lunar year of 12 months"""
leapYear = lunarYear + lunarMonth
"""The lenght of a leap year of 13 months"""
cycleYears = 19
"""In a cycle of 19 lunar years with 7 leap years, the number of days is the same as 19 solar years"""
cycle = lunarYear * 12 + leapYear * 7
"""The length of a 19 lunar year cycle with 7 leap years"""
leapYears = [3, 6, 8, 11, 14, 17, 19]
"""The leap years in a 19 year cycle are years 3, 6, 8, 11, 14, 17, and 19"""

class year:
    """Holds the year number from Creation, 
    the cycles past and place in cycle, 
    the date and day of the week of Rosh Hashana, 
    and the list of whole months."""

    # 1) Take the number of years from the year of creation.
    def __init__(self, count: int, startYear = 1) -> None:
        # startYear being 0 means that this is an internal calculation instance of the year class, and we won't want to calculate if its length, only it's Rosh Hashana day, for the needs of the previous year. 
        if startYear == 1 or startYear == 0:
            self.yearsFromCreation = count
            """The number of years from year 1 = the year of BHRD"""
        
        # If the year count is not from creation, determin the number of years from creation. 
        else:
            self.yearsFromCreation = startYear - 1 + count
            # E.g. if the starting year is 2 (the year of Man's creation) and the year is 1, then it is two years in the count from the creation year.

        # 2) Divide that into cycles. We now know the number of cycles and the year within the current cycle.
    
        # Since we will have to correct for the last year of  the cycle, first determin the year within the cycle.
        self.placeInCycle = self.yearsFromCreation % cycleYears
        """The place in the 19 year cycle from 1-19"""
        if self.placeInCycle == 0:
            self.cyclesToYear = self.yearsFromCreation // cycleYears - 1
            """The number of whole 19 year cycles before the current year"""
            self.placeInCycle = cycleYears
        else:
            self.cyclesToYear = self.yearsFromCreation // cycleYears
    
        # 3) Add together the full cycles
        self.molad = BHRD + cycle * self.cyclesToYear
        """The molad of the begning of this year"""
        
        # (The Rambam says to do this by adding the weekly movements. That is easier for finding the molad in days of the week. However, I have done the calculation with the full number of days since the comupter doesn't care and this is needed for later calculations.)

        # 4) Add the regular years and the leap years

        # The given year does not get its length added to the total time. This is accomplished by the for loop itself; the place in cycle is out of the range.
        for y in range(1, self.placeInCycle):
            if y in leapYears:
                self.molad = self.molad + leapYear
            else:
                self.molad = self.molad + lunarYear
    
        #(Halacha 15 is in the month class)

        # Defining Rosh Hashana of the year
        #7:1
        ADU = [1,4,6]
        """The day of Rosh Chodesh Tishrei (Rosh Hashanah) is never set to days 1, 4, or 6, according to the set calandar. """
        # When the molad would have it so, Rosh Chodesh is set to the next day.   
        if self.molad.days % 7 in ADU:
            self.roshHashanahDate = self.molad.days + 1
            """The date of Rosh Hashanah of this year, in days from the Shabbos before BHRD"""

        #7:2
        # If the molad is after noon, Rosh Chodesh is set to the next day, if the next day is not 1, 4 or 6.
        elif self.molad.hours >= 18:
            if self.molad.days % 7 + 1 not in ADU:
                self.roshHashanahDate = self.molad.days + 1
        
        #7:3
        # If the molad is after noon and the next day is 1, 4, or 6, Rosh Chodesh is two days after the molad.
            else:
                self.roshHashanahDate = self.molad.days + 2

        #7:4 
        # GTRD - If the molad of Tishrei is on a day 3, and the molad is after 9 hours and 204 chalakim, and the year is not a  leap year, Rosh Chodesh is set to day 5, which is two days after the molad. 
        elif ((self.molad.days % 7 == 3)
         and ((self.molad.hours > 9) or ((self.molad.hours == 9) and (self.molad.chalakim >= 204)))
         and (self.placeInCycle not in leapYears)):
            self.roshHashanahDate = self.molad.days + 2

        #7:5 
        # BTU TKPT - If the molad of Tishrei is on a day 2, and the molad is after 15 hours and 589 chalakim, and it is the year after a  leap year, Rosh Chodesh is set to day 3. 
        elif ((self.molad.days % 7 == 2)
         and ((self.molad.hours > 15) or ((self.molad.hours == 15) and (self.molad.chalakim >= 589)))
         and ((self.placeInCycle - 1 in leapYears) or (self.placeInCycle - 1 == 0))):
            self.roshHashanahDate = self.molad.days + 1
        
        #7:6
        # If none of the cases applies, Rosh Hashana is on the day of the molad. 
        else:
            self.roshHashanahDate = self.molad.days
        
        self.roshHashanahDay = self.roshHashanahDate % 7
        """The day of the week of Rosh Hashanash of this year, from 1-7"""
        if self.roshHashanahDay == 0: self.roshHashanahDay = 7
        
        #8:3 
        # Since the length of a lunar month is not exactly 29 1/2 days, some years have more whole months than short months and (as a result of pushing off Rosh Hashana) some years have more short months than whole months.
        #8:5
        # The months that are always set by the fixed calandar are Nissan 30, Iyyar 29, Sivan 30, Tamuz 29, Av 30, Elul 29, Tishrei 30, Teves 29, Shevat 30, Addar (II) 29.
        
        # (This list of whole months starts with Tishrei, and assumes that Marheshvan will be lacking and Kislev will be full.)
        self.wholeMonths = [True, False, True, False, True, False,
                            True, False, True, False, True, False]
        """Those months that are whole in this year. True = whole"""
        # In a leap year Addar I is a full month.
        if self.placeInCycle in leapYears: self.wholeMonths.insert(5, True)
        
        #8:6
        yearType = { 'full' : False, 'lacking' : False, 'orderly' : False}
        """An indicator if the current year's months (Marhesvan and Kislev) are lacking, whole, or accorting to thier normal pattern, Marheshvan lacking and Kislev whole."""
        
        #8:7
        # Determinimg the type of year for setting the days of Rosh Chodesh of the different months.
        if startYear != 0:
            dummyYear = True
            """Tells the newly created year not to unnessicarily calculate its own month lenght arangement (and avoid and infinate recurtion) by setting the start year to 0"""
            daysBetween = (self.yearAfter(dummyYear).roshHashanahDay - self.roshHashanahDay -1) % 7
            """The number of days between Rosh Hashanah this year and Rosh Hashana next year, not inclusive"""
            if self.placeInCycle not in leapYears:
                #For different days between, set different year types
                try: yearType[{2: 'lacking', 3: 'orderly', 4: 'full'}[daysBetween]] = True
                except KeyError as d:
                    print("There are", d, "days between Rosh HaShana of year", self.yearsFromCreation,"and the next year's. Is this year GTRD?")
            
            #8:8
            else:   #On a leap year:
                try: yearType[{4: 'lacking', 5: 'orderly', 6: 'full'}[daysBetween]] = True
                except KeyError as d:
                    print("There are", d, "days between Rosh HaShana of year", self.yearsFromCreation,"and the next year's. Is this next year BTU TKPT?")

        # (8:6) The months of Marheshvan and Kislev are variable.
        # Tishrei is month 0 
        if yearType['lacking']: self.wholeMonths[2] = False
        if yearType['full']: self.wholeMonths[1] = True
    
    def yearAfter (self, dummyYear = False):
        """Generates the next year after this one"""
        return year(self.yearsFromCreation + 1, (0 if dummyYear else 1))