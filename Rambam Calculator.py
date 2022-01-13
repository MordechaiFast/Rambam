from calendarUnits import *

def printMonthsOfYear (aYear: Year, printNextTishrei = False):
    """Prints all of the months of the given year, with their names, molad, and days of Rosh Chodesh."""

    for thisMonth in aYear:
        if thisMonth.two_day_Rosh_Chodesh():
            if thisMonth.day_of_week() == 1:
                print(thisMonth.name, "\t", thisMonth.molad,"\t", 7,1)
            else:
                print(thisMonth.name, "\t", thisMonth.molad, "\t", thisMonth.day_of_week() - 1, thisMonth.day_of_week())
        else:
            print(thisMonth.name, "\t", thisMonth.molad, "\t", thisMonth.day_of_week())
    if printNextTishrei:
        thisMonth = Month(aYear.yearAfter(), 7)
        print(thisMonth.name, "\t", thisMonth.molad, "\t", thisMonth.day_of_week())

RambamsYear = Year(4938)
print("The year the Ramabam was writing was:", RambamsYear.yearsFromCreation)
print("That was cycle", RambamsYear.cyclesToYear + 1, " year", RambamsYear.placeInCycle, "\n")
printMonthsOfYear(RambamsYear)