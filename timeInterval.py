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

    # comparison functions
    def __eq__(self, __o: object) -> bool:
        if ( self.days == __o.days 
         and self.hours == __o.hours 
         and self.chalakim == __o.chalakim):
            return True
        else: return False

    def __ge__(self, __o: object) -> bool:
        if self.days > __o.days:
            return True
        elif self.days == __o.days:
            if self.hours > __o.hours:
                return True
            elif self.hours == __o.hours:
                if self.chalakim >= __o.chalakim:
                    return True
        return False

    #math functions
    def __add__(self,addtime):
        if type(addtime) is tuple:
            # In case of a tuple of 0 or one number, compleate the tuple to three places.
            addtime += (0,0,0)
            addtime = timeInterval(addtime[0], addtime[1], addtime[2])
        elif not isinstance(addtime, timeInterval):
            raise TypeError("Can only add timeInterval or tuple")

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
        if type(minustime) is tuple:
            minustime += (0,0,0)
            minustime = timeInterval(minustime[0], minustime[1], minustime[2])
        elif not isinstance(minustime, timeInterval):
            raise TypeError("Can only subtract timeInterval or tuple")

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

    def __add__(self, addtime):
        return timeInWeek(super().__add__(addtime))
    def __mul__(self, factor):
        return timeInWeek(super().__mul__(factor))
    def __sub__(self, minustime):
        return timeInWeek(super().__sub__(minustime))
    def __floordiv__(self, divisor):
        return timeInWeek(super().__floordiv__(divisor))

t=timeInterval(-1,-1,-1)