#!/usr/bin/env python
from classes.calendarUnits import Day, Year, Month

def printMonthsOfYear(aYear: Year, printNextTishrei = False):
    """Prints all of the months of the given year, with their names, molad, and days of Rosh Chodesh."""

    for thisMonth in aYear:
        Rosh_Chodesh = Day(thisMonth)
        if thisMonth.two_day_Rosh_Chodesh:
            if Rosh_Chodesh.day_of_week == 1:
                print(f"{thisMonth.name:10} {thisMonth.molad}  7 1")
            else:
                print(f"{thisMonth.name:10} {thisMonth.molad}  "
                f"{Rosh_Chodesh.day_of_week - 1} {Rosh_Chodesh.day_of_week}")
        else:
            print(f"{thisMonth.name:10} {thisMonth.molad}  "
            f"{Rosh_Chodesh.day_of_week}")
    if printNextTishrei:
        thisMonth = Month(aYear.year_after, 7)
        Rosh_Chodesh = Day(thisMonth)
        print(f"{thisMonth.name:10} {thisMonth.molad}  "
        f"{Rosh_Chodesh.day_of_week}")

RambamsYear = Year(4938)
print("The year the Ramabam was writing was:", RambamsYear.years_from_creation)
print("That was cycle", RambamsYear.cycles_to_year + 1, " year", RambamsYear.place_in_cycle, "\n")
printMonthsOfYear(RambamsYear)

printMonthsOfYear(Year(int(input('Year: '))))