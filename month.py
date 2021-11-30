from year import year, leapYears, lunarMonth

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

        # Convert month from Nissan to months from Tishrei, when neccesary
        if startFromTishrei:
            self.monthCount = monthReference
            """The number of this month from Tishrei = 0"""
        else:
            # For months between Tishrei and Nissan: 
            if monthReference > 6:
                # We want Tishrei to be 0, so take away 7.
                self.monthCount = monthReference - 7
            # For months between Nissan and Tishrei, it depends if the given year is a leap year.
            elif year.placeInCycle in leapYears:
                # Nissan is 7 months from Tishrei in a leap year.
                self.monthCount = monthReference + 6
            else:
                # Nissan is 6 months from Tishrei in a regular year.
                self.monthCount = monthReference + 5
    
        #6:15
        # To find the molad of a specific month, add the molad of a month for each month until the requiered month.
        self.molad = year.molad.add(lunarMonth.multiply(self.monthCount))

        # Defning the day of Rosh Chodesh
        #8:1-2 
        # A month can only be of whole days.
        shortMonth = 29
        """Some months are lacking and have 29 days"""
        wholeMonth = 30
        """Some months are whole and have 30 days."""

        #8:4
        # For a month following a full month, Rosh Chodesh is two days.
        # (I don't have a nice way to fit Tishrei into this, so it is here a seperate condition) 
        if self.monthCount == 0:
            self.twoDayRoshChodesh = False
            """Whether or not this month has a two day Rosh Chodesh"""
        elif year.wholeMonths[self.monthCount-1]:
            self.twoDayRoshChodesh = True
        else:
            self.twoDayRoshChodesh = False

        # Working out the date of Rosh Chodesh for the month, and the day of the week. (Not worked out in Rambam.)
        # Start with the first month: Rosh Chodesh Tishrei is Rosh Hashana. 
        self.roshChodeshDate = year.roshHashanahDate
        """The date of Rosh Chodesh of this month, in days from 
        the Shabbos before BHRD"""

        for i in range (self.monthCount):
            if year.wholeMonths[i]:
                self.roshChodeshDate += wholeMonth
            else:
                self.roshChodeshDate += shortMonth
        self.roshChodeshDay = self.roshChodeshDate % 7
        """The day of the week of Rosh Chodesh of this month, 1-7"""
        if self.roshChodeshDay == 0: self.roshChodeshDay = 7