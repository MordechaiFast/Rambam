# Perek 6 - The molad

#6:1
# The first step in calculating the moon sighting for a given month is to work out how many days after a date with known solar and lunar positions. In order to to that we must work out the aproximate date of conjunction, the molad.
 
from timeInterval import timeInterval

#sample time printing
def printTime (title, time:timeInterval, space = False):
    """Prints the title on the first line, the days, hours and chalakim of the given time on the second line, and a blank line if requested."""

    print (title)
    print ("Days:", time.days, "Hours:", time.hours, "Chalakim:", time.chalakim)
    if space: print("")
space = True

print ("\nRambam calulations\n")

#6:3
from year import lunarMonth
printTime("One month is:", lunarMonth, space)

#6:4
# The length of the various types of years.
from year import lunarYear, leapYear
from season import season, solarYear, solarYearExcess
#"""
printTime("Twevle months is:", lunarYear)
printTime("Thirteen months is:", leapYear)
printTime("A solar year is:", solarYear)
printTime("That is more than a lunar year by:", solarYearExcess, space)
#"""

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

#6:6-8
exampleMonth = timeInterval(1,17,107)
"""
printTime("For example, if molad Nissan is:", exampleMonth)
printTime("Molad Iyyar will be:", exampleMonth.add(lunarMonthInWeek), space)
printTime("Molad Nissan the next year will be:", exampleMonth.add(lunarYearInWeek), space)
"""

from year import BHRD
printTime("BHRD was:", BHRD, space)

#6:9
# When adding the movements in the week, one must reduce the chalakim, hours and days.
#printTime("The molad of Tishrei after BHRD was, after rounding:", BHRD.add(lunarYearInWeek).inWeek(), space)

#6:10
from year import cycleYears, cycle
from season import solarCycle, solarCycleExcess
#"""
printTime("One 19 year cycle is:", cycle)
printTime("One solar cycle is:", solarCycle)
printTime("That is more than a lunar cycle by:", solarCycleExcess, space)
#"""

#6:11
from year import leapYears
print("The leap years are:", leapYears, "\n")

#6:12
cycleInWeek = (lunarYearInWeek.multiply(12)).add(leapYearInWeek.multiply(7)).inWeek()
"""The length of a cycle in days of the week."""
#printTime("Each cycle moves the molad:", cycleInWeek, space)

#6:13
# Adding a cycle's days of the week gets you the next cycle.
#printTime("After BHRD the next cycle began:", BHRD.add(cycleInWeek), space)

#6:14
# Given a year, find the molad for the start of that year.
from year import year
#"""
RambamsYear = year(4938)
print("The year the Ramabam was writing was:", RambamsYear.yearsFromCreation)
print ("That was cycle", RambamsYear.cyclesToYear + 1, " year", RambamsYear.placeInCycle, "\n")
#"""

#6:15
# For any month, find the molad of that month.
from month import month

monthNames = ["Tishrei", "Marchesvan", "Kislev ", "Teves  ", "Shevat ", "Addar  ",
"Nissan ", "Iyyar  ", "Sivan  ", "Tamuz  ", "Av     ", "Elul   "]
monthNamesInLeapYear = ["Tishrei", "Marchesvan", "Kislev ", "Teves  ", "Shevat ",
"Addar I", "Addar II", "Nissan ", "Iyyar  ", "Sivan  ", "Tamuz  ", "Av     ", "Elul   "]
printNextTishrei = True
startFromTishrei = True

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
        if thisMonth.twoDayRoshChodesh:
            if thisMonth.roshChodeshDay == 1: print(names[m], "\t", thisMonth.molad.inWeek().days, thisMonth.molad.hours, thisMonth.molad.chalakim,"\t", 7,1)
            else: print(names[m], "\t", thisMonth.molad.inWeek().days, thisMonth.molad.hours, thisMonth.molad.chalakim, "\t", thisMonth.roshChodeshDay - 1, thisMonth.roshChodeshDay)
        else: print(names[m], "\t", thisMonth.molad.inWeek().days, thisMonth.molad.hours, thisMonth.molad.chalakim, "\t", thisMonth.roshChodeshDay)
    if printNextTishrei:
        thisMonth = month(aYear.yearAfter(), 7)
        print(monthNames[0], "\t", thisMonth.molad.inWeek().days, thisMonth.molad.hours, thisMonth.molad.chalakim, "\t", thisMonth.roshChodeshDay)

#"""
for y in [5745, 5765, 5766]:
    print("\nYear", y)
    printMonthsOfYear(year(y), printNextTishrei)
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
printTime("Some say the lenght of a solar year is:", solarYear, space)
#9:2
from season import seasonLength
printTime("19 solar years are then in excess of the lunar years by:", solarCycleExcess)
printTime("A standard season lenght is:", seasonLength, space)
 #9:5
exampleSeason = season(year(4930))
printTime("The Nissan season of 4930", exampleSeason.time)