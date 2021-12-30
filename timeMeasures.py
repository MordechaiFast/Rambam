from itertools import zip_longest

# Defining a time interval and how to calculate with it
class TimeInterval:
    """Used for the lenght of a month, year, etc."""

    def __init__(self, days=0, hours=0, chalakim=0):
        self.days = days
        self.hours = hours
        self.chalakim = chalakim

        # For converting a TimeInterval to a TimeInWeek, a TimeInterval gets passed to the new object. To handel that:
        if isinstance(days, TimeInterval):
            self.days = days.days
            self.hours = days.hours
            self.chalakim = days.chalakim

        self.reduce()

    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Converts fractional parts of days and hours to hours and chalakim. Does not affect the day count."""
        #6:2
        HOURS_IN_DAY = 24
        """The day is broken up into 24 hours. """
        CHALAKIM_IN_HOUR = 1080
        """The hour is broken up into 1080 chalakim (parts). This is just a number that has many divisors."""

        #6:9
        # Convert fractional days into hours
        self.hours += (self.days % 1) * HOURS_IN_DAY
        self.days = int(self.days // 1)
        
        # Convert fractional hours into chalakim
        self.chalakim += (self.hours % 1) * CHALAKIM_IN_HOUR
        self.hours = int(self.hours // 1)

        # Fractional chalakim will be ignored untill the subclass fine time interval
        self.chalakim = int(self.chalakim // 1)

        # Carry the whole hours, then round the remaining chalakim. (This also works for negetive inputs.)
        self.hours += self.chalakim // CHALAKIM_IN_HOUR
        self.chalakim %= CHALAKIM_IN_HOUR
        
        # Carry the whole days, then round the remaining hours.
        self.days += self.hours // HOURS_IN_DAY
        self.hours %= HOURS_IN_DAY

    # iteration function
    def __iter__(self) -> int:
        yield from [self.days, self.hours, self.chalakim]

    # String function
    def __str__(self) -> str:
        return f"{self.days} {self.hours:>2} {self.chalakim:>4}"
        
    # The following methods should work unchanged in a four item subclass.
    # comparison functions
    def __eq__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if x == y: continue
            else: return False
        else: return True

    def __gt__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if   x >  y: return True
            elif x == y: continue
            else: return False
        else: return False

    def __ge__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if   x >  y: return True
            elif x == y: continue            
            else: return False
        return True

    def __lt__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if   x <  y: return True
            elif x == y: continue          
            else: return False
        else: return False

    # math functions
    def __add__(self, addend):
        sum = [x + y for x, y in zip_longest(self, addend, fillvalue= 0)]
        return type(self)(sum[0], sum[1], sum[2])
 
    def __sub__(self, subtrahend):
        difference = [x - y for x, y in zip_longest(self, subtrahend, fillvalue= 0)]
        return type(self)(difference[0], difference[1], difference[2])

    def __mul__(self, factor):
        product = [x * factor for x in self]
        return type(self)(product[0], product[1], product[2])

    def __floordiv__(self, divisor):
        quotent = [x / divisor for x in self]
        return type(self)(quotent[0], quotent[1], quotent[2])

class TimeInWeek (TimeInterval):
    """A time of week, or the offset of a time of week."""
    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Sets the day to a day of the week 1-7."""
        super().reduce()
        self.days %= 7
        # We want Shabbos to be appear as 7, even though its mod is 0.
        if self.days == 0 : self.days = 7