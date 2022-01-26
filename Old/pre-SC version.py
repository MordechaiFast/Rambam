# Perek 6 - The molad

#6:1
# The first step in calculating the moon sighting for a given
# month is to work out how many days after a date with known
# solar and lunar positions. In order to to that we must work 
# out the aproximate date of conjunction, the molad.
 
#6:2
hoursInDay = 24
"""The day is broken up into 24 hours. """
chalakimInHour = 1080
"""The hour is broken up into 1080 chalakim (parts). This is just a number that has many divisors."""

# Defining a time interval and how to calculate with it
class timeInterval:
    """Used for the lenght of a month or year, a molad, 
    or the movement of the molad from one date to another.
    Dates are in days after Shabbos before BHRD."""

    def __init__(self, days=0, hours=0, chalakim=0):
        self.days = days
        self.hours = hours
        self.chalakim = chalakim
        self.reduce()

    # Used in 6:5 and onwards.
    def inWeek(self):
        """Returns the time by the day of the week.
        Shabbos is returned as 7"""

        dayOfWeek = self.days % 7

        # We want Shabbos to be appear as 7, even though its 
        # mod is 0.
        if dayOfWeek != 0:
            return timeInterval(dayOfWeek, self.hours, self.chalakim)
        else:
            return timeInterval(7, self.hours, self.chalakim)

    #6:9
    def reduce(self):
        """Reduces the number of chalakim to less than 1080 
        and the hours to less than 24, adding the whole hours 
        and whole days. Does not affect the day count."""
        
        # First carry the whole hours, then round the remaining chalakim. 
        self.hours += self.chalakim // chalakimInHour
        self.chalakim = self.chalakim % chalakimInHour
        # Next carry the whole days, then round the remaining hours.
        self.days += self.hours // hoursInDay
        self.hours = self.hours % hoursInDay

    #math functions
    def add(self, addtime):
        new = timeInterval()
        new.days = self.days + addtime.days
        new.hours = self.hours + addtime.hours
        new.chalakim = self.chalakim + addtime.chalakim
        new.reduce()
        return new
    
    def multiply(self, factor:int):
        new = timeInterval()
        new.days = self.days * factor
        new.hours = self.hours * factor
        new.chalakim = self.chalakim * factor
        new.reduce()
        return new
    
    def subtract(self, minustime):
        new = timeInterval()
        borrowHour = False
        borrowDay = False

        #subtract the chalakim
        if self.chalakim >= minustime.chalakim:
            new.chalakim = self.chalakim - minustime.chalakim
        else:
            borrowHour = True
            new.chalakim = self.chalakim + chalakimInHour - minustime.chalakim
        
        #subtract the hours
        if borrowHour:
            if self.hours - 1 >= minustime.hours:
                new.hours = self.hours - 1 - minustime.hours
            else:
                borrowDay = True
                new.hours = self.hours + hoursInDay - 1 - minustime.hours
        else:
            if self.hours >= minustime.hours:
                new.hours = self.hours - minustime.hours
            else:
                borrowDay = True
                new.hours = self.hours + hoursInDay - minustime.hours
        
        #subtract the days
        if borrowDay:
            new.days = self.days - 1 - minustime.days
        else:
            new.days = self.days - minustime.days
        
        new.reduce()
        return new

#sample time printing
def printTime (title, time:timeInterval, space = False):
    print (title)
    print ("Days:", time.days, ", Hours: ", time.hours, ", Chalakim: ", time.chalakim)
    if space: print("")
space = True
print ("\nRambam calulations\n")

#6:3
lunarMonth = timeInterval(29,12,793)
"""The length of a month"""
#printTime("One month is:", lunarMonth, space)

#6:4
# The length of the various types of years.
lunarYear = lunarMonth.multiply(12)
"""The lenght of a lunar year of 12 months"""
leapYear = lunarYear.add(lunarMonth)
"""The lenght of a leap year of 13 months"""
solarYear = timeInterval(365,6)
"""The lenght of a year of 365.25 days"""
solarYearExcess = solarYear.subtract(lunarYear)
"""The excess of a 365.25 day year over a 12 month year"""
#printTime("Twevle months is:", lunarYear)
#printTime("Thirteen months is:", leapYear)
#printTime("A solar year is:", solarYear)
#printTime("That is more than a lunar year by:", solarYearExcess, space)

#6:5
lunarMonthInWeek = lunarMonth.inWeek()
"""The ofset of the molad after one month"""
lunarYearInWeek = lunarYear.inWeek()
"""The ofset of the molad after one regular year"""
leapYearInWeek = leapYear.inWeek()
"""The ofset of the molad after one leap year"""
"""
printTime("Each month moves the molad:", lunarMonthInWeek)
printTime("Each regular year:", lunarYearInWeek)
printTime("Each leap year:", leapYearInWeek, space)
#"""

#6:6
# Adding a month by days of the week. This is the
# add method of the class, with lunarMonthInWeek.

#6:7-8
exampleMonth = timeInterval(1,17,107)
"""
printTime("For example, if molad Nissan is:", exampleMonth)
printTime("Molad Iyyar will be:", exampleMonth.add(lunarMonthInWeek), space)
printTime("Molad Nissan the next year will be:", exampleMonth.add(lunarYearInWeek), space)
"""

BHRD = timeInterval(2,5,204)
"""Starting molad"""
#printTime("BHRD was:", BHRD, space)

#6:9
# When adding the movements in the week, one must 
# reduce the chalakim, hours and days.
"""
printTime("The molad of Tishrei after BHRD was, after rounding:", BHRD.add(lunarYearInWeek).inWeek(), space)
#"""

#6:10
cycleYears = 19
"""In a cycle of 19 lunar years with 7 leap years, the number of days is the same as 19 solar years"""
cycle = (lunarYear.multiply(12)).add(leapYear.multiply(7))
"""The length of a 19 lunar year cycle with 7 leap years"""
solarCycle = solarYear.multiply(cycleYears)
"""The lenght of 19 years of 365.25 days"""
"""
printTime("One 19 year cycle is:", cycle)
printTime("One solar cycle is:", solarCycle)
printTime("That is more than a lunar cycle by:", solarCycle.subtract(cycle), space)
#"""

#6:11

leapYears = [3, 6, 8, 11, 14, 17, 19]
"""The leap years in a 19 year cycle are years 3, 6, 8, 11, 14, 17, and 19"""
#print("The leap years are:", leapYears, \n)

#6:12
cycleInWeek = (lunarYearInWeek.multiply(12)).add(leapYearInWeek.multiply(7)).inWeek()
"""The length of a cycle in days of the week."""
#printTime("Each cycle moves the molad:", cycleInWeek, space)

#6:13
# Adding a cycle's days of the week gets you the next cycle.
#printTime("After BHRD the next cycle began:", BHRD.add(cycleInWeek), space)

#6:14
# Given a year, find the molad for the start of that year.

# This class needs cycle, cycleYears, and BHRD.
class year:
    """Holds the year number from Creation, 
    the cycles past and place in cycle, 
    the date and day of the week of Rosh Hashana, 
    and the list of whole months."""

    # 1) Take the number of years from the year of creation.
    def __init__(self, count: int, startYear = 1) -> None:
        # startYear being 0 means that this is an internal calculation 
        # instance of the year class, and we won't want to calculate if
        # its length, only it's Rosh Hashana day, for the needs of the
        # previous year. 
        if startYear == 1 or startYear == 0:
            self.yearsFromCreation = count
            """The number of years from year 1 = the year of BHRD"""
        
        # If the year count is not from creation, determin the
        # number of years from creation. 
        else:
            self.yearsFromCreation = startYear - 1 + count
            # E.g. if the starting year is 2 (the year of Man's 
            # creation) and the year is 1, then it is two years
            # in the count from the creation year.

        # 2) Divide that into cycles. We now know the number
        #    of cycles and the year within the current cycle.
    
        # Since we will have to correct for the last year of 
        # the cycle, first determin the year within the cycle.
        self.placeInCycle = self.yearsFromCreation % cycleYears
        """The place in the 19 year cycle from 1-19"""
        if self.placeInCycle == 0:
            self.cyclesToYear = self.yearsFromCreation // cycleYears - 1
            self.placeInCycle = cycleYears
        else:
            self.cyclesToYear = self.yearsFromCreation // cycleYears
    
        # 3) Add together the full cycles
        self.molad = BHRD.add(cycle.multiply(self.cyclesToYear))
        """The molad of the begning of this year"""
        
        # (The Rambam says to do this by adding the weekly movements. 
        # That is easier for finding the molad in days of the week. 
        # However, I have done the calculation with the full number 
        # of days since the comupter doesn't care and this is needed 
        # for later calculations.)

        # 4) Add the regular years and the leap years

        # The given year does not get its length added to the 
        # total time. This is accomplished by the for loop itself; 
        # the place in cycle is out of the range.
        for y in range(1, self.placeInCycle):
            if y in leapYears:
                self.molad = self.molad.add(leapYear)
            else:
                self.molad = self.molad.add(lunarYear)
    
        #(Halacha 15 is in the month class)
   
    def yearAfter (self, dummyYear = False):
        """Generates the next year after this one"""
        return year(self.yearsFromCreation + 1, (0 if dummyYear else 1))
        

startFromTishrei = True
class month:
    """monthReference starts with 0 for Tishrei or 1 for Nissan.
    Holds the year that the month is in, 
    the month's number starting from Tishrei, 
    the molad of that month, 
    and the date and day of Rosh Chodesh."""
    
    def __init__(self, year: year, monthReference: int, startFromTishrei = False) -> None:
        #Save the year
        self.year = year
        """The year that this month is a part of"""

        # Convert month from Nissan to months from Tishrei, when 
        # neccesary
        if startFromTishrei:
            self.monthCount = monthReference
            """The number of this month from Tishrei = 0"""
        else:
            # For months between Tishrei and Nissan: 
            if monthReference > 6:
                # We want Tishrei to be 0, so take away 7.
                self.monthCount = monthReference - 7
            # For months between Nissan and Tishrei, it depends if the 
            # given year is a leap year.
            elif year.placeInCycle in leapYears:
                # Nissan is 7 months from Tishrei in a leap year.
                self.monthCount = monthReference + 6
            else:
                # Nissan is 6 months from Tishrei in a regular year.
                self.monthCount = monthReference + 5
    
        #6:15
        # To find the molad of a specific month, add the molad
        # of a month for each month until the requiered month.
        self.molad = year.molad.add(lunarMonth.multiply(self.monthCount))
        
#6:14
"""
RambamsYear = year(4938)
print("The year the Ramabam was writing was:", RambamsYear.yearsFromCreation)
print ("That was cycle", RambamsYear.cyclesToYear + 1, " year", RambamsYear.placeInCycle)
#"""

#6:15
monthNames = ["Tishrei", "Marchesvan", "Kislev ", "Teves  ", "Shevat ", "Addar  ",
"Nissan ", "Iyyar  ", "Sivan  ", "Tamuz  ", "Av     ", "Elul   "]
monthNamesInLeapYear = ["Tishrei", "Marchesvan", "Kislev ", "Teves  ", "Shevat ",
"Addar I", "Addar II", "Nissan ", "Iyyar  ", "Sivan  ", "Tamuz  ", "Av     ", "Elul   "]
printNextTishrei = True
def printMonthsOfYear (aYear: year, printNextTishrei = False):
    """Prints all of the months of the given year, with their
    names, molad, and days of Rosh Chodesh."""
    if aYear.placeInCycle not in leapYears:
        n = 12
        names = monthNames
    else:
        n = 13
        names = monthNamesInLeapYear
    for m in range (n):
        thisMonth = month(aYear, m, startFromTishrei)
        print(monthNames[m], "\t", thisMonth.molad.inWeek().days, thisMonth.molad.hours, thisMonth.molad.chalakim)
    if printNextTishrei:
        thisMonth = month(aYear.yearAfter(), 7)
        print(monthNames[0], "\t", thisMonth.molad.inWeek().days, thisMonth.molad.hours, thisMonth.molad.chalakim)

for y in [5745, 5765, 5766]:
    print("\nYear", y)
    printMonthsOfYear(year(y), printNextTishrei)