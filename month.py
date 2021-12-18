from calendarUnits import Year, LEAP_YEARS, LUNAR_MONTH_REMAINDER
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