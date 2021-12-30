# Perek 6 - The molad

#6:1
# The first step in calculating the moon sighting for a given month is to work out how many days after a date with known solar and lunar positions. In order to to that we must work out the aproximate date of conjunction, the molad.
 
from timeMeasures import TimeInterval

#sample time printing
def printTime (title, time:TimeInterval, space = False):
    """Prints the title on the first line, the days, hours and chalakim of the given time on the second line, and a blank line if requested."""

    print (title)
    print ("Days:", time.days, "Hours:", time.hours, "Chalakim:", time.chalakim)
    if space: print("")
space = True

print ("\nRambam calulations\n")

#6:3
from calendarUnits import LUNAR_MONTH
#printTime("6:3 One month is:", lunarMonth, space)

#6:4
# The length of the various types of years.
from calendarUnits import LUNAR_YEAR, LEAP_YEAR
from season import SOLAR_YEAR, SOLAR_YEAR_EXCESS
"""
printTime("6:4 Twevle months is:", lunarYear)
printTime("Thirteen months is:", leapYear)
printTime("A solar year is:", solarYear)
printTime("That is more than a lunar year by:", solarYearExcess, space)
#"""

#6:5
from calendarUnits import LUNAR_MONTH_REMAINDER, LUNAR_YEAR_REMAINDER, LEAP_YEAR_REMAINDER 
"""
printTime("6:5 Each month moves the molad:", lunarMonthRemainder)
printTime("Each regular year:", lunarYearRemainder)
printTime("Each leap year:", leapYearRemainder, space)
#"""

#6:6-8
exampleMonth = TimeInterval(1,17,107)
"""
printTime("6:7 For example, if molad Nissan is:", exampleMonth)
printTime("Molad Iyyar will be:", exampleMonth + lunarMonthRemainder, space)
printTime("6:8 Molad Nissan the next year will be:", exampleMonth + lunarYearRemainder, space)
#"""

from calendarUnits import BHRD
#printTime("6:8 BHRD was:", BHRD, space)

#6:9
# When adding the movements in the week, one must reduce the chalakim, hours and days.
printTime("6:9 The molad of Tishrei after BHRD was, after rounding:", BHRD + LUNAR_YEAR_REMAINDER, space)

#6:10
from calendarUnits import CYCLE_YEARS, CYCLE
from season import SOLAR_CYCLE, SOLAR_CYCLE_EXCESS
"""
printTime("6:10 One 19 year cycle is:", cycle)
printTime("One solar cycle is:", solarCycle)
printTime("That is more than a lunar cycle by:", solarCycleExcess, space)
#"""

#6:11
from calendarUnits import LEAP_YEARS
#print("6:11 The leap years are:", leapYears, "\n")

#6:12
from calendarUnits import CYCLE_REMAINDER
#printTime("6:12 Each cycle moves the molad:", cycleRemainder, space)

#6:13
# Adding a cycle's days of the week gets you the next cycle.
# printTime("6:13 After BHRD the next cycle began:", BHRD + cycleRemainder, space)

#6:14
# Given a year, find the molad for the start of that year.
from calendarUnits import Year

RambamsYear = Year(4938)
"""
print("6:14 The year the Ramabam was writing was:", RambamsYear.yearsFromCreation)
print("That was cycle", RambamsYear.cyclesToYear + 1, " year", RambamsYear.placeInCycle, "\n")
#"""

#6:15
# For any month, find the molad of that month.
from calendarUnits import Month

printNextTishrei = True
startFromTishrei = True
def printMonthsOfYear (aYear: Year, printNextTishrei = False):
    """Prints all of the months of the given year, with their names, molad, and days of Rosh Chodesh."""

    for m in range (12 if aYear.placeInCycle not in LEAP_YEARS else 13):
        thisMonth = Month(aYear, m, startFromTishrei)
        if thisMonth.twoDayRoshChodesh:
            if thisMonth.day == 1:
                print(thisMonth.name, "\t", thisMonth.molad,"\t", 7,1)
            else:
                print(thisMonth.name, "\t", thisMonth.molad, "\t", thisMonth.day - 1, thisMonth.day)
        else:
            print(thisMonth.name, "\t", thisMonth.molad, "\t", thisMonth.day)
    if printNextTishrei:
        thisMonth = Month(aYear.yearAfter(), 7)
        print(thisMonth.name, "\t", thisMonth.molad, "\t", thisMonth.day)

# """ GTRD and BTU TKPT testing
dummyYear = 0
for y in [5745, 5765]:
    print("\nYear", y)
    try: 
        printMonthsOfYear(Year(y), printNextTishrei)
    except KeyError as d:
        if d.args[0] == 5: print("GTRD")
        if d.args[0] == 3: print("BTU TKPT")
        print("There are", d, "days between Rosh HaShana of year", y, "and the next year's. Is this year GTRD or next year BTU TKPT?")
        printMonthsOfYear(Year(y, dummyYear), printNextTishrei)        
#"""

# Perek 7 - The day of Rosh HaShanah
# (Halachaos 1-6 are in the year class.)

#7:7
# The reason for pushing off some days is to (sometimes) get the actual day of conjunction to be on the day set as Rosh Chodesh.
# 
# An example:
# SET THE MOLAD FOR (4,12) AND SHOW THAT AN ECLIPSE WILL BE ON DAY 5

#7:8
# Also the pushing off of GTRD is to (occasionally) put the day of conjunction on Rosh Chodesh.
# 
# An example:
# SET MOLAD FOR (3,11) AND SHOW THAT THE MOON IS NOT VISABLE ON DAY 6 

#Perek 8 - The day of Rosh Chodesh

#8:4
#print ("8:4 Tishrei is a two day rosh chodesh", month(RambamsYear, 7).twoDayRoshChodesh)

#8:9
"""Find a year where Rosh Hashanah is on 5 and next year's is on 2, not leap year
for y in range(1,6000):
    myYear = year(y)
    if myYear.roshHashanahDay == 5 and myYear.yearAfter().roshHashanahDay == 2 and myYear.placeInCycle not in leapYears:
        break
print ("The Rambam's example first occurs on year:", myYear.yearsFromCreation)
"""

#Perek 9 - the seasons by the even measure
#9:1
#printTime("Some say the lenght of a solar year is:", solarYear, space)
#9:2
from season import SEASON_LENGTH
#printTime("19 solar years are then in excess of the lunar years by:", solarCycleExcess)
#printTime("A standard season lenght is:", seasonLength, space)

#9:5
"""
for y in range(4922, 4930):
    exampleYear = year(y)
    exampleMonth = month(exampleYear,1)
    exampleSeason = season(exampleYear)
    print("Year", y)
    printTime("The molad of Nissan is", exampleMonth.molad)
    print("That is year", exampleYear.placeInCycle, "of its cycle.")
    printTime("The Nissan season is", exampleSeason.time, space)
"""