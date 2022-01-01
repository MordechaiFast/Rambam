from itertools import zip_longest
# Defining a time interval and how to calculate with it
class TimeInterval:
    """Used for the lenght of a month, year, etc."""

    def __init__(self, days=0, hours=0, chalakim=0):
        self.days = days
        self.hours = hours
        self.chalakim = chalakim
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
        # Set the chalakim
        self.reduce_chalakim()
        # Carry the whole hours, then round the remaining chalakim. (This also works for negetive inputs.)
        self.hours += self.chalakim // CHALAKIM_IN_HOUR
        self.chalakim %= CHALAKIM_IN_HOUR        
        # Carry the whole days, then round the remaining hours.
        self.days += self.hours // HOURS_IN_DAY
        self.hours %= HOURS_IN_DAY

    def reduce_chalakim(self):
        # Fractional chalakim will be ignored untill the subclass FineTimeInterval
        self.chalakim = int(self.chalakim // 1)

    # iteration function
    def __iter__(self) -> int:
        yield from [self.days, self.hours, self.chalakim]

    # String function
    def __str__(self) -> str:
        return f"{self.days} {self.hours:>2} {self.chalakim:>4}"
        
    # The following methods work unchanged in a four item subclass.
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
        return type(self)(*[x + y
         for x, y in zip_longest(self, addend, fillvalue= 0)])
    def __sub__(self, subtrahend):
        return type(self)(*[x - y 
         for x, y in zip_longest(self, subtrahend, fillvalue= 0)])
    def __mul__(self, factor):
        return type(self)(*[x * factor for x in self])
    def __floordiv__(self, divisor):
        return type(self)(*[x / divisor for x in self])
    def __truediv__(self, divisor):
        return FineTimeInterval(*[x / divisor for x in self],
         regaim_total= divisor)

class TimeInWeek (TimeInterval):
    """A time of week, or the offset of a time of week."""
    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Sets the day to a day of the week 1-7."""
        super().reduce()
        self.days %= 7
        # We want Shabbos to be appear as 7, even though its mod is 0.
        if self.days == 0 : self.days = 7

class FineTimeInterval(TimeInterval):
    """A Time interval with divisons of less than a chailek. The precision is set by the defining division.
    
    WARNING: Using two bases at once will cause errors."""
    regaim_total = 0    # A class variable shared by all active instences.
    
    def __init__(self, days=0, hours=0, chalakim=0, regaim=0,
     regaim_total=None):
        if regaim_total:
            FineTimeInterval.regaim_total = regaim_total

        self.regaim = regaim
        super().__init__(days=days, hours=hours, chalakim=chalakim)
    
    def reduce_chalakim(self):
       # Convert fractional chalkim to regaim
        self.regaim += int((self.chalakim % 1) * self.regaim_total)
        self.chalakim = int(self.chalakim // 1)

        # Carry the whole chalakim, then round the remaining regaim.
        self.chalakim += self.regaim // self.regaim_total
        self.regaim %= self.regaim_total

    # String function
    def __str__(self) -> str:
        return f"{self.days} {self.hours:>2} {self.chalakim:>4} {self.regaim:>2}"

    # iteration function
    def __iter__(self) -> int:
        yield from [self.days, self.hours, self.chalakim, self.regaim]