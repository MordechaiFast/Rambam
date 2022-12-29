"""Defining a time interval and how to calculate with it"""

from itertools import zip_longest

#6:2
HOURS_IN_DAY = 24
"""The day is broken up into 24 hours. """

class TimeInterval:
    """Used for the lenght of a month, year, etc."""
    parts_in_hour = 1   
    # A class variable. Could conceviably be set to any value.

    def __init__(self, days=0, hours=0, parts=0, *, parts_in_hour=None):
        if parts_in_hour:   
        # 0 would cause a division by zero, so rule that out too.
            TimeInterval.parts_in_hour = parts_in_hour
        self.days = days
        self.hours = hours
        self.parts = parts
        self.reduce()

    def reduce(self):
        """Reduce the number of parts to less than an hour, etc.
        
        Reduces the number of parts to less than an hour and the hours 
        to less than 24, adding the whole hours and whole days. Converts 
        fractional parts of days and hours to hours and parts. Does not 
        affect the whole day count."""
        #6:9
        # Convert fractional days into hours
        self.hours += (self.days % 1) * HOURS_IN_DAY
        self.days = int(self.days // 1)
        # Convert fractional hours into parts
        self.parts += (self.hours % 1) * TimeInterval.parts_in_hour
        self.hours = int(self.hours // 1)
        # Set the parts
        self.reduce_parts()
        # Carry the whole hours, then round the remaining parts.
        # (This also works for negetive inputs.)
        self.hours += self.parts // TimeInterval.parts_in_hour
        self.parts %= TimeInterval.parts_in_hour        
        # Carry the whole days, then round the remaining hours.
        self.days += self.hours // HOURS_IN_DAY
        self.hours %= HOURS_IN_DAY

    def reduce_parts(self):
        # Fractional parts will be ignored
        # untill the subclass FineTimeInterval
        self.parts = int(self.parts // 1)

    # Iteration function
    def __iter__(self) -> int:
        yield from [self.days, self.hours, self.parts]

    # Hash function
    def __hash__(self) -> int:
        return hash((self.days, self.hours, self.parts, self.parts_in_hour))
    # String functions
    def __str__(self) -> str:
        return f"{self.days} {self.hours:2} {self.parts:4}"
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.days}, {self.hours}, "
        f"{self.parts}, parts_in_hour={self.parts_in_hour})")
        
    # The following methods work unchanged in a four item subclass.
    # absolute value
    def __abs__(self):
        return self * -1 if self < type(self)(0) else self

    # comparison functions
    def __eq__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if x == y:
                continue
            else:
                return False
        return True

    def __gt__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if   x >  y:
                return True
            elif x == y:
                continue
            else: # x < y
                return False
        # if x == y for all
        return False

    def __ge__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if   x >  y:
                return True
            elif x == y:
                continue            
            else: # x < y
                return False
        # if x == y for all
        return True

    def __lt__(self, other) -> bool:
        for x, y in zip_longest(self, other, fillvalue= 0):
            if   x <  y:
                return True
            elif x == y:
                continue          
            else: # x > y
                return False
        # if x == y for all
        return False

    # math functions
    def __add__(self, addend):
        return type(self)(*[x + y
         for x, y in zip_longest(self, addend, fillvalue= 0)])
    def __radd__(self, addend):
        return type(self)(*[x + y
         for x, y in zip_longest(addend, self, fillvalue= 0)])
    def __sub__(self, subtrahend):
        return type(self)(*[x - y 
         for x, y in zip_longest(self, subtrahend, fillvalue= 0)])
    def __mul__(self, factor):
        return type(self)(*[x * factor for x in self])
    def __rmul__(self, factor):
        return type(self)(*[x * factor for x in self])
    def __floordiv__(self, divisor):
        return type(self)(*[x / divisor for x in self])
    def __truediv__(self, divisor):
        return FineTimeInterval(*[x / divisor for x in self],
         moments_in_part= divisor)

class TimeInWeek (TimeInterval):
    """A time of week, or the offset of a time of week."""
    def reduce(self):
        """Sets the day to a day of the week to 1-7."""
        super().reduce()
        self.days %= 7
        # We want Shabbos to be appear as 7, even though its mod is 0.
        if self.days == 0:
            self.days = 7

class FineTimeInterval(TimeInterval):
    """A Time interval with divisons of less than a chailek.
    
    The precision is set by the defining division.
    
    WARNING: Using two bases at once will cause errors."""
    moments_in_part = 1    
    # A class variable shared by all active instences.
    
    def __init__(self, days=0, hours=0, parts=0, moments=0, *,
     moments_in_part=None):
        if moments_in_part:
        # 0 would cause a division by zero, so rule that out too.
            FineTimeInterval.moments_in_part = moments_in_part
        self.moments = moments
        super().__init__(days=days, hours=hours, parts=parts)
    
    def reduce_parts(self):
        """Convert fractional parts to moments"""
        self.moments += (self.parts % 1) * self.moments_in_part
        self.parts = int(self.parts // 1)
        # Truncate fractional moments
        self.moments = int(self.moments // 1)
        # Carry the whole parts, then round the remaining moments.
        self.parts += self.moments // self.moments_in_part
        self.moments %= self.moments_in_part

    # Iteration function
    def __iter__(self) -> int:
        yield from [self.days, self.hours, self.parts, self.moments]

    # String function
    def __str__(self) -> str:
        return f"{self.days} {self.hours:2} {self.parts:4} {self.moments:2}"

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.days}, {self.hours}, "
        f"{self.parts}, {self.moments}, moments_in_part="
        f"{self.moments_in_part})")

    def __truediv__(self, divisor):
        raise TypeError(f"Not supported for {self.__class__.__name__}")