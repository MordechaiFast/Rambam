from classes.timeMeasures import TimeInWeek, TimeInterval

# Constants
CHALAKIM_IN_HOUR = 1080
"""The hour is broken up into 1080 chalakim (parts). This is just a number that has many divisors."""
LUNAR_MONTH = TimeInterval(29,12,793, parts_in_hour= CHALAKIM_IN_HOUR)
"""The length of a month, (29, 12, 793)"""
LUNAR_YEAR = LUNAR_MONTH * 12
"""The lenght of a lunar year of 12 months, (354, 8, 876)"""
LEAP_YEAR = LUNAR_MONTH * 13
"""The lenght of a leap year of 13 months, (383, 21, 589)"""
LUNAR_MONTH_REMAINDER = TimeInWeek(*LUNAR_MONTH)
"""The offset of the molad after one month, (1, 12, 793)"""
LUNAR_YEAR_REMAINDER = LUNAR_MONTH_REMAINDER * 12
"""The offset of the molad after one regular year, (4, 8, 876)"""
LEAP_YEAR_REMAINDER = LUNAR_MONTH_REMAINDER * 13
"""The offset of the molad after one leap year, (5, 21, 589)"""
BHRD = TimeInWeek(6,14) - LUNAR_YEAR_REMAINDER
"""The molad of the end of the year of creation was (6, 14, 0), so the 
molad of the begining of that year was (2, 5, 204)."""
CYCLE_YEARS = 19
"""In a cycle of 19 lunar years with 7 leap years, the number of days 
is the same as 19 solar years"""
CYCLE = LUNAR_YEAR * 12 + LEAP_YEAR * 7
"""The length of a 19 lunar year cycle with 7 leap years"""
CYCLE_REMAINDER = LUNAR_YEAR_REMAINDER * 12 + LEAP_YEAR_REMAINDER * 7
"""The length of a cycle in days of the week."""
LEAP_YEARS = {0, 3, 6, 8, 11, 14, 17, 19}
"""The leap years in a 19 year cycle are years 3, 6, 8, 11, 14, 17, and 19."""
ADU = {1,4,6}
"""The day of Rosh Chodesh Tishrei (Rosh Hashanah) is never set to days 
1, 4, or 6, according to the set calandar."""
GTRD = TimeInWeek(7,18) - LUNAR_YEAR_REMAINDER
"""If the molad of this year is after (3, 9, 204), and this year is a 
non-leap year, next year's molad will end up being on day 7 after noon, 
which gets pushed off to day 2, which makes too many whole monts for 
our calandar, so we push off the beginging of this year."""
BTU_TKPT = TimeInWeek(3, 18) + LEAP_YEAR_REMAINDER
"""When a leap year begins on day 3 after noon, Rosh Hashana is pushed 
off to day 5, but next year's molad is on day 2, and sometimes before 
noon. In that case, there would be too few whole months for our 
calandar, so we push off the following year's Rosh Hashana."""

class Year:
    """Holds the year number from Creation, the cycles past and place 
    in cycle.

    Can calculate the date and day of the week of Rosh Hashana, and the 
    list of whole months."""

    def __init__(self, count: int, start_year=1) -> None:
        self.years_from_creation = start_year - 1 + count
        """The number of years from year 1 = the year of BHRD"""
        # E.g. if the starting year is 2 (the year of Man's creation) 
        # and the year is 1, then it is two years in the count from the 
        # creation year.
        self._calc_molad()
        # Always calculate the molad of the year. This is needed for 
        # everyhting else.
        self._Rosh_Hashana_day = None
        """The day of the week of Rosh Hashanah of this year from 1-7"""
        self._date = None
        """The date of Rosh Hashanah of this year in days from Shabbos 
        before BHRD"""
        self._whole_months = None
        """Those months that are whole in this year. True == whole"""

    def _calc_molad(self):
        # 6:14
        # 1) Take the number of years from the year of creation.
        # 2) Divide that into cycles. We now know the number of cycles 
        # and the year within the current cycle.
        self.cycles_to_year = self.years_from_creation // CYCLE_YEARS
        """The number of whole 19 year cycles before the current year"""
        self.place_in_cycle = self.years_from_creation % CYCLE_YEARS
        """The place in the 19 year cycle from 1-19"""
        # Correct for 0 in mod 19
        if self.place_in_cycle == 0:
            self.cycles_to_year -= 1
            self.place_in_cycle = CYCLE_YEARS
    
        # 3) Add together the full cycles
        self.molad =  CYCLE_REMAINDER * self.cycles_to_year + BHRD
        """The molad of the begning of this year"""
        
        # 4) Add the regular years and the leap years
        for y in range(1, self.place_in_cycle):
            if y in LEAP_YEARS:
                self.molad += LEAP_YEAR_REMAINDER
            else:
                self.molad += LUNAR_YEAR_REMAINDER

    def __repr__(self) -> str:
        return f"Year({self.years_from_creation})"
    
    def __iter__(self):
        yield from [Month(self, n, start_from_Tishrei=True) for n in range
         (12 if self.place_in_cycle not in LEAP_YEARS else 13)]
    
    @property
    def year_after(self):
        """Generates the next year after this one."""
        return Year(self.years_from_creation + 1)
        
    @property
    def Rosh_Hashana(self) -> int:
        """Returns the day of the week of Rosh Hashana of this year."""
        if self._Rosh_Hashana_day is not None:
            return self._Rosh_Hashana_day
        #7:1
        # The day of Rosh Chodesh Tishrei (Rosh Hashanah) is never set 
        # to days 1, 4, or 6, according to the set calandar. When the 
        # molad would have it so, Rosh Chodesh is set to the next day.   
        if self.molad.days in ADU:
            self._Rosh_Hashana_day = self.molad.days + 1
        #7:2
        # If the molad is after noon, Rosh Chodesh is set to the next 
        # day, if the next day is not 1, 4 or 6.
        elif self.molad.hours >= 18:
            if self.molad.days % 7 + 1 not in ADU:
            # mod needed in case day is 7, to set it to 0
                self._Rosh_Hashana_day = self.molad.days + 1
                # We know that the day is not 7, so no need to mod.     
        #7:3
        # If the molad is after noon and the next day is 1, 4, or 6, 
        # Rosh Chodesh is two days after the molad.
            elif self.molad.days % 7 + 1 in ADU:
            # Realy just else, but keeping to the Rambam text.
                self._Rosh_Hashana_day = self.molad.days % 7 + 2
        #7:4 
        # GTRD - If the molad of Tishrei is on a day 3, and the molad 
        # is after 9 hours and 204 chalakim, and the year is not a leap 
        # year, Rosh Chodesh is set to day 5, which is two days after 
        # the molad. 
        elif (self.molad.days == 3
          and self.molad >= GTRD
          and self.place_in_cycle not in LEAP_YEARS):
            self._Rosh_Hashana_day = self.molad.days + 2
        #7:5 
        # BTU TKPT - If the molad of Tishrei is on a day 2, and the 
        # molad is after 15 hours and 589 chalakim, and it is the year 
        # after a leap year, Rosh Chodesh is set to day 3. 
        elif (self.molad.days == 2
          and self.molad >= BTU_TKPT
          and self.place_in_cycle - 1 in LEAP_YEARS):
            self._Rosh_Hashana_day = self.molad.days + 1
        #7:6
        # If none of the cases applies, Rosh Hashana is on the day of 
        # the molad. 
        else:
            self._Rosh_Hashana_day = self.molad.days
        return self._Rosh_Hashana_day

    @property
    def date(self) -> int:
        """ Calculates the date of Rosh Hashana of this year in days from 
        the Shabbos before BHRD."""
        if self._date is None:
            objective_molad = CYCLE * self.cycles_to_year + BHRD
            """The molad in days from Shabbos before BHRD"""
            for y in range(1, self.place_in_cycle):
                if y in LEAP_YEARS:
                    objective_molad += LEAP_YEAR
                else:
                    objective_molad += LUNAR_YEAR
            self._date = (objective_molad.days 
            + self.Rosh_Hashana - self.molad.days % 7)
        return self._date
    
    @property
    def whole_months(self) -> list:
        """Returns a list of the months in this year that are whole 
        (30 days), starting with Tishrei."""
        if self._whole_months is not None:
            return self._whole_months
        #8:3 
        # If the length of a month was exactly 29.5 days, the months 
        # would go one whole and one short.
        self._whole_months = [True, False] * 6
        # (This list of whole months starts with Tishrei, and assumes 
        # that Marheshvan will be lacking and Kislev will be full.)
        # Since the length of a lunar month is not exactly 29 1/2 days, 
        # some years have more whole months than short months and (as 
        # a result of pushing off Rosh Hashana) some years have more 
        # short months than whole months.
        #8:5
        # The months that are always set by the fixed calandar are 
        # Nissan 30, Iyyar 29, Sivan 30, Tamuz 29, Av 30, Elul 29, 
        # Tishrei 30, Teves 29, Shevat 30, Addar (II) 29. In a leap 
        # year Addar I is a full month.
        if self.place_in_cycle in LEAP_YEARS:
            self._whole_months.insert(5, True)
        #8:6
        # Determinimg the type of year for setting the days of Rosh 
        # Chodesh of the different months.
        # If the current year's months (Marhesvan and 
        # Kislev) are lacking, whole, or accorting to thier normal 
        # pattern, Marheshvan lacking and Kislev whole.
        #8:7
        days_between = (self.year_after.Rosh_Hashana 
                       - self.Rosh_Hashana - 1) % 7
        """The number of days between Rosh Hashanah this year and 
        Rosh Hashana next year, not inclusive"""
        
        #8:7-8
        #For different days between, set different year types
        year_type = (     {2: 'lacking', 3: 'orderly', 4: 'full'}
                     if   self.place_in_cycle not in LEAP_YEARS
                     else {4: 'lacking', 5: 'orderly', 6: 'full'}
                    )[days_between]
        # (8:6) The months of Marheshvan and Kislev are variable.
        if   year_type == 'lacking':
            self._whole_months[2] = False     # Tishrei is month 0 
        elif year_type == 'full':
            self._whole_months[1] = True
        return self._whole_months

MONTH_NAMES = ["Tishrei", "Marchesvan", "Kislev", "Teves", "Shevat", "Addar",
"Nissan", "Iyyar", "Sivan", "Tamuz", "Av", "Elul"]
MONTH_NAMES_IN_LEAP_YEAR = ["Tishrei", "Marchesvan", "Kislev", "Teves", 
"Shevat", "Addar I", "Addar II", "Nissan", "Iyyar", "Sivan", "Tamuz", "Av", 
"Elul"]
#8:1-2 
# A month can only be of whole days.
SHORT_MONTH, WHOLE_MONTH = 29, 30

class Month:
    """monthReference starts with 0 for Tishrei or 1 for Nissan.

    Holds the year that the month is in, 
    the month's name, 
    the molad of that month, 
    and the date and day of the week Rosh Chodesh."""
    
    def __init__(self, year: Year, month_reference: int, *,
     start_from_Tishrei=False) -> None:
        # Save the year
        self.year = year
        """The year that this month is a part of"""
        # Convert month from Nissan to months from Tishrei, when neccesary
        if start_from_Tishrei:
            self.month_count = month_reference
            """The number of this month from Tishrei = 0"""
        else:
            # For months between Tishrei and Nissan: 
            if month_reference > 6:
                # We want Tishrei to be 0, so take away 7.
                self.month_count = month_reference - 7
            # For months between Nissan and Tishrei, it depends if the 
            # given year is a leap year.
            elif year.place_in_cycle in LEAP_YEARS:
                # Nissan is 7 months from Tishrei in a leap year.
                self.month_count = month_reference + 6
            else:
                # Nissan is 6 months from Tishrei in a regular year.
                self.month_count = month_reference + 5
        # Find the month's name
        self.name = (MONTH_NAMES[self.month_count]
                if   year.place_in_cycle not in LEAP_YEARS
                else MONTH_NAMES_IN_LEAP_YEAR[self.month_count])
        """The name of the month"""
        # Don't calculate the date untill asked
        self._date = None
        """The date of Rosh Chodesh of this month"""
    
        #6:15
        # To find the molad of a specific month, add the molad of a 
        # month for each month until the requiered month.
        self.molad = year.molad + LUNAR_MONTH_REMAINDER * self.month_count
        """The molad of this month"""

    def __str__(self) -> str:
        return f"{self.name} {self.year.years_from_creation}"

    @property
    def two_day_Rosh_Chodesh(self) -> bool:
        """Returns the True if Rosh Chodesh of this month is two days, False if not."""
        #8:4
        # For a month following a full month, Rosh Chodesh is two days.
        return self.year.whole_months[self.month_count-1]
        # [-1] returns the last item in the list, which is what we want.

    @property
    def is_whole(self) -> bool:
        """Returns True if this month has 30 days"""
        return self.year.whole_months[self.month_count]

    @property
    def date(self) -> int:
        """Returns out the date of Rosh Chodesh for the month, in days from the Shabbos before BHRD."""
        if self._date is None:
            # Start with the first month: Rosh Chodesh Tishrei is Rosh Hashana. 
            self._date = self.year.date
            for monthIsWhole in self.year.whole_months[:self.month_count]:
                self._date += WHOLE_MONTH if monthIsWhole else SHORT_MONTH
        return self._date

    @property
    def month_after(self):
        """Generates the next month after this one."""
        if self.month_count < 11 or (
           self.year.place_in_cycle in LEAP_YEARS and self.month_count == 11):
            return Month(self.year, self.month_count + 1)
        else: # must be last month of the year
            return Month(self.year.year_after, 7)
        
class Day:
    def __init__(self, month: Month, day: int = 1) -> None:
        self.month = month
        self.day = day
    
    def __add__(self, addend: int):
        day = self.day + addend
        month = Month(self.month.year, self.month.month_count,
                      start_from_Tishrei=True)
        while day > (days_in_month := 30 if month.is_whole else 29):
            day -= days_in_month
            month = month.month_after
        return type(self)(month, day)

    @classmethod
    def from_date(cls, date: int):
        d = TimeInterval(date)
        year_count = 1
        month_count = 0
        while d > CYCLE:
            year_count += CYCLE_YEARS
            d -= CYCLE
        for y in range(1, CYCLE_YEARS+1):
            year_lenght = LEAP_YEAR if y in LEAP_YEARS else LUNAR_YEAR
            if d > year_lenght:
                year_count += 1
                d -= year_lenght
            else:
                break
        while d > LUNAR_MONTH:
            # Rosh Chodesh can never be eariler than the day of the molad
            month_count += 1
            d -= LUNAR_MONTH
        month = Month(Year(year_count), month_count,
                        start_from_Tishrei=True)
        day = date - month.date+1
        if day < 1:
            # Rosh Chodeh is later than the molad this month,
            # so the calendar month is one back 
            if month_count > 0:
                month = Month(Year(year_count), month_count - 1,
                        start_from_Tishrei=True)
            else:
                month = Month(Year(year_count - 1), 6) #Elul
            day = date - month.date+1
        return cls(month, day)

    def __str__(self) -> str:
        return f"{self.day} {self.month}"

    @property
    def date(self) -> int:
        return self.month.date-1 + self.day

    @property
    def day_of_week(self) -> int:
        return self.date % 7 if self.date % 7 != 0 else 7