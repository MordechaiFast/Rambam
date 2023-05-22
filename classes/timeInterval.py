from classes.base_class import MeasureWithSubunits

class TimeInterval(MeasureWithSubunits):
    units = {'days': 7, 'hours': 24, 'parts': 1080}

    def __str__(self) -> str:
        return f"{self.days} {self.hours:2} {self.parts:4}"

class TimeInWeek(TimeInterval):
    cycle = True

    def __init__(self, *args, units: dict = None) -> None:
        super().__init__(*args, units=units)
        if self.days == 0:
            self.__dict__['days'] = 7

class FineTimeInterval(TimeInterval):
    def __str__(self) -> str:
        return f"{self.days} {self.hours:2} {self.parts:4} {self.moments:2}"

TimeInterval.child_class = FineTimeInterval

class Degrees(MeasureWithSubunits):
    units = {'degrees': 360, 'minutes':60, 'seconds': 60}
    strict = False

    def __str__(self) -> str:
        return (f"{self.degrees}\N{DEGREE SIGN}"
                f"{self.minutes:02}'{self.seconds:02}\"")
    
class Degrees3(Degrees):
    units = Degrees.units | {'thirds': 60}
    
    def __eq__(self, other) -> bool:
        """Allows comparison between this and a normal Degrees object, 
        with this rounded to the nearest second or truncated to the second."""
        if super().__eq__(other):
            return True
        elif not self.strict:
            return (
                    self.degrees == other[0]
                and self.minutes == other[1]
                and (self.seconds == other[2]
                    or (self.seconds + 1 == other[2]
                        and self.thirds >= self.units['thirds'] /2))
            )
        else:
            return False
    
    __hash__ = Degrees.__hash__

Degrees.child_class = Degrees3

class Degrees4(Degrees3):
    units = Degrees3.units | {'fourths': 60}

Degrees3.child_class = Degrees4

class DegreesOfCircle(Degrees4):
    cycle = True

DegreesOfCircle.child_class = DegreesOfCircle
