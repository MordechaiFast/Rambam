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
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Does not affect the day count."""
        
        # First carry the whole hours, then round the remaining chalakim. 
        self.hours += self.chalakim // chalakimInHour
        self.chalakim %= chalakimInHour
        # Next carry the whole days, then round the remaining hours.
        self.days += self.hours // hoursInDay
        self.hours %= hoursInDay

    #math functions
    def __add__(self,addtime):
        new = timeInterval()
        new.days = self.days + addtime.days
        new.hours = self.hours + addtime.hours
        new.chalakim = self.chalakim + addtime.chalakim
        new.reduce()
        return new
 
    def __mul__(self, factor):
        new = timeInterval()
        new.days = self.days * factor
        new.hours = self.hours * factor
        new.chalakim = self.chalakim * factor
        new.reduce()
        return new

    def __sub__(self, minustime):
        new = timeInterval()
        borrowHour = False
        borrowDay = False

        #subtract the chalakim
        if self.chalakim >= minustime.chalakim:
            new.chalakim = self.chalakim - minustime.chalakim
        else:
            borrowHour = True
            new.chalakim = self.chalakim + chalakimInHour - minustime.chalakim
        
        #subtract the hours
        if borrowHour:
            if self.hours - 1 >= minustime.hours:
                new.hours = self.hours - 1 - minustime.hours
            else:
                borrowDay = True
                new.hours = self.hours + hoursInDay - 1 - minustime.hours
        else:
            if self.hours >= minustime.hours:
                new.hours = self.hours - minustime.hours
            else:
                borrowDay = True
                new.hours = self.hours + hoursInDay - minustime.hours
        
        #subtract the days
        if borrowDay:
            new.days = self.days - 1 - minustime.days
        else:
            new.days = self.days - minustime.days
        
        new.reduce()
        return new

    def __floordiv__(self, divisor):
        new = timeInterval()
        new.days = self.days // divisor
        hourDivident = self.hours + (self.days % divisor * hoursInDay)
        new.hours = hourDivident // divisor
        chalakimDivident = self.chalakim + (hourDivident % divisor * chalakimInHour)
        new.chalakim = chalakimDivident // divisor
        new.reduce()
        return new

class timeInWeek (timeInterval):
    """A time of week"""
    def __init__(self, totalTime: timeInterval):
        super().__init__(days=totalTime.days, hours=totalTime.hours, chalakim=totalTime.chalakim)

    def reduce(self):
        """Reduces the number of chalakim to less than 1080 and the hours to less than 24, adding the whole hours and whole days. Sets the day to a day of the week 1-7."""

        super().reduce()
        self.days %= 7
        # We want Shabbos to be appear as 7, even though its mod is 0.
        if self.days == 0 : self.days = 7

    def __add__(self, addtime):
        return timeInWeek(super().__add__(addtime))
    def __mul__(self, factor):
        return timeInWeek(super().__mul__(factor))
    def __sub__(self, minustime):
        return timeInWeek(super().__sub__(minustime))
    def __floordiv__(self, divisor):
        return timeInWeek(super().__floordiv__(divisor))