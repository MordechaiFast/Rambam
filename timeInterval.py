#6:2
HOURS_IN_DAY = 24
"""The day is broken up into 24 hours. """
CHALAKIM_IN_HOUR = 1080
"""The hour is broken up into 1080 chalakim (parts). This is just a number that has many divisors."""

# Defining a time interval and how to calculate with it
class timeInterval:
    """Used for the lenght of a month, year, etc."""

    def __init__(self, days=0, hours=0, chalakim=0):
        self.days = days
        self.hours = hours
        self.chalakim = chalakim
        self.reduce()

    FULL_LENGTH = 3
    """How many places this type of time measure accepts."""

    #6:9
    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Converts fractional parts of days and hours to hours and chalakim. Does not affect the day count."""
        # Convert fractional days into hours
        self.hours += (self.days % 1) * HOURS_IN_DAY
        self.days //= 1
        
        # Convert fractional hours into chalakim
        self.chalakim += (self.hours % 1) * CHALAKIM_IN_HOUR
        self.hours //= 1

        # Fractional chalakim will be ignored untill the subclass fine time interval
        self.chalakim //= 1

        # Carry the whole hours, then round the remaining chalakim. (This also works for negetive inputs.)
        self.hours += self.chalakim // CHALAKIM_IN_HOUR
        self.chalakim %= CHALAKIM_IN_HOUR
        
        # Carry the whole days, then round the remaining hours.
        self.days += self.hours // HOURS_IN_DAY
        self.hours %= HOURS_IN_DAY

    # iteration functions
    def __getitem__(self, key) -> int:
        if   key == 0: return self.days
        elif key == 1: return self.hours
        elif key == 2: return self.chalakim
        else: raise IndexError
    def __setitem__(self, key, value):
        if   key == 0: self.days = value
        elif key == 1: self.hours = value
        elif key == 2: self.chalakim = value
        else: raise IndexError

    # Allow operators to work with tuples
    def tuple_check(self, input, operation: str):
        if type(input) is tuple:
            # In case of a tuple of less than three numbers, compleate the tuple to three places.
            input += (0,0,0)
            input = timeInterval(input[0], input[1], input[2])
        elif not isinstance(input, timeInterval):
            raise TypeError("Can only " + operation + " timeInterval or tuple")
        return input

    # The following methods should work unchanged in a four item subclass.
    def __len__(self):
        for i in range (self.FULL_LENGTH -1, -1, -1):
            if self[i]: return i + 1
        else: return 0

    # comparison functions
    def __eq__(self, other) -> bool:
        other = self.tuple_check(other, "compare")
        
        for i in range(self.FULL_LENGTH):
            if self[i] == other[i]: continue
            else: return False
        else: return True

    def __ge__(self, other) -> bool:
        other = self.tuple_check(other, "compare")
        
        for i in range(self.FULL_LENGTH):
            if   self[i] >  other[i]: return True
            elif self[i] == other[i]: continue
            else: return False
        return True

    def __lt__(self, other) -> bool:
        other = self.tuple_check(other, "compare")
        
        for i in range(self.FULL_LENGTH):
            if   self[i] <  other[i]: return True
            elif self[i] == other[i]: continue
            else: return False
        else: return False

    #math functions
    def __add__(self, addend):
        addend = self.tuple_check(addend, "add")

        sum = timeInterval()
        for i in range (self.FULL_LENGTH):
            sum[i] = self[i] + addend[i]
        sum.reduce()
        return sum
 
    def __sub__(self, subtrahend):
        subtrahend = self.tuple_check(subtrahend, "subtract")

        difference = timeInterval()
        for i in range (self.FULL_LENGTH -1, -1, -1):
            difference[i] = self[i] + -subtrahend[i]
        difference.reduce()
        return difference

    def __mul__(self, factor):
        product = timeInterval()
        for i in range(len(self)):
            product[i] = self[i] * factor
        product.reduce()
        return product

    def __floordiv__(self, divisor):
        return self * (1 / divisor)
    
    # String function
    def __str__(self) -> str:
        return f"{self.days} {self.hours:>2} {self.chalakim:>4}"

class timeInWeek (timeInterval):
    """A time of week, or the offset of a time of week."""
    def __init__(self, totalTime: timeInterval):
        super().__init__(days=totalTime.days, hours=totalTime.hours, chalakim=totalTime.chalakim)

    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Sets the day to a day of the week 1-7."""

        super().reduce()
        self.days %= 7
        # We want Shabbos to be appear as 7, even though its mod is 0.
        if self.days == 0 : self.days = 7

    def __add__(self, addend):
        return timeInWeek(super().__add__(addend))
    def __mul__(self, factor):
        return timeInWeek(super().__mul__(factor))
    def __sub__(self, subtrahend):
        return timeInWeek(super().__sub__(subtrahend))
    def __floordiv__(self, divisor):
        return timeInWeek(super().__floordiv__(divisor))