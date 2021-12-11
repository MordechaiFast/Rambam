#6:2
hoursInDay = 24
"""The day is broken up into 24 hours. """
chalakimInHour = 1080
"""The hour is broken up into 1080 chalakim (parts). This is just a number that has many divisors."""

# Defining a time interval and how to calculate with it
class timeInterval:
    """Used for the lenght of a month, year, etc."""

    def __init__(self, days=0, hours=0, chalakim=0):
        self.days = days
        self.hours = hours
        self.chalakim = chalakim
        self.reduce()

    #6:9
    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Converts fractional parts of days and hours to hours and chalakim. Does not affect the day count."""
        # Convert fractional days into hours
        self.hours += (self.days % 1) * hoursInDay
        self.days //= 1
        
        # Convert fractional hours into chalakim
        self.chalakim += (self.hours % 1) * chalakimInHour
        self.hours //= 1

        # Fractional chalakim will be ignored untill the subclass fine time interval
        self.chalakim //= 1

        # Carry the whole hours, then round the remaining chalakim. (This also works for negetive inputs.)
        self.hours += self.chalakim // chalakimInHour
        self.chalakim %= chalakimInHour
        
        # Carry the whole days, then round the remaining hours.
        self.days += self.hours // hoursInDay
        self.hours %= hoursInDay

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
    def __len__(self):
        if   self[2]: return 3
        elif self[1]: return 2
        elif self[0]: return 1
        else: return 0

    # comparison functions
    def __eq__(self, other) -> bool:
        if type(other) is tuple:
            # In case of a tuple of 0 or one number, compleate the tuple to three places.
            other += (0,0,0)
            other = timeInterval(other[0], other[1], other[2])
        elif not isinstance(other, timeInterval):
            raise TypeError("Can only compare timeInterval or tuple")
        for i in range(3):
            if self[i] == other[i]: continue
            else: return False
        return True

    def __ge__(self, other) -> bool:
        if type(other) is tuple:
            # In case of a tuple of 0 or one number, compleate the tuple to three places.
            other += (0,0,0)
            other = timeInterval(other[0], other[1], other[2])
        elif not isinstance(other, timeInterval):
            raise TypeError("Can only compare timeInterval or tuple")
        for i in range(3):
            if self[i] > other[i]: return True
            elif self[i] == other[i]: continue
            else: return False
        return True

    #math functions
    def __add__(self,addend):
        if type(addend) is tuple:
            # In case of a tuple of 0 or one number, compleate the tuple to three places.
            addend += (0,0,0)
            addend = timeInterval(addend[0], addend[1], addend[2])
        elif not isinstance(addend, timeInterval):
            raise TypeError("Can only add timeInterval or tuple")

        sum = timeInterval()
        sum.days = self.days + addend.days
        sum.hours = self.hours + addend.hours
        sum.chalakim = self.chalakim + addend.chalakim
        sum.reduce()
        return sum
 
    def __sub__(self, subtrahend):
        if type(subtrahend) is tuple:
            subtrahend += (0,0,0)
            subtrahend = timeInterval(subtrahend[0], subtrahend[1], subtrahend[2])
        elif not isinstance(subtrahend, timeInterval):
            raise TypeError("Can only subtract timeInterval or tuple")

        return self + (-subtrahend.days, -subtrahend.hours, -subtrahend.chalakim)

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