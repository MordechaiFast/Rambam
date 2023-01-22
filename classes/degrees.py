from itertools import zip_longest
from math import isclose
from .timeMeasures import TimeInterval

DEGREES_IN_CIRCLE = 360
PARTS_IN_DEGREE = 60

class Degrees(TimeInterval):
    """Class for holding and working with circle measures"""

    def __init__(self, degrees=0, *parts):
        self.degrees = degrees
        # Always set minutes and seconds
        if   len(parts) >  1:
            self.parts = [*parts]
        elif len(parts) == 1:
            self.parts = [*parts, 0]
        else: #len(parts) == 0
            self.parts = [0, 0]
        self.reduce()

    def reduce(self):
        # Convert fractional degrees into minutes
        self.parts[0] += (self.degrees % 1) * PARTS_IN_DEGREE
        self.degrees = int(self.degrees // 1)
        # Convert fractional minutes into seconds, etc.
        for n in range(len(self.parts) - 1):
            self.parts[n+1] += (self.parts[n] % 1) * PARTS_IN_DEGREE
            self.parts[n] = int(self.parts[n] // 1)
        # Round a round float (from 60 times the modulus)
        if isclose(self.parts[-1], round(self.parts[-1]), abs_tol=1/360000):
            self.parts[-1] = round(self.parts[-1])
        # Carry the whole minutes from the seconds, etc.
        for n in range(len(self.parts), 1, -1):
            self.parts[n-2] += int(self.parts[n-1] // PARTS_IN_DEGREE)
            self.parts[n-1] %= PARTS_IN_DEGREE
        # Carry the whole degrees from the minutes
        self.degrees += self.parts[0] // PARTS_IN_DEGREE
        self.parts[0] %= PARTS_IN_DEGREE
        while self.parts[-1] == 0 and len(self.parts) > 2:
            del self.parts[-1]

    def __hash__(self) -> int:
        return hash((self.degrees, *self.parts))
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.degrees}, {self.parts})"
    def __str__(self) -> str:
        rounded_seconds = (int(self.parts[1])
                           if len(self.parts) < 3
                           else self.parts[1]
                                if self.parts[2] < 30
                                else int(self.parts[1]) + 1)
        return (f"{self.degrees}\N{DEGREE SIGN}{int(self.parts[0]):2}'"
                f"{rounded_seconds:2}\"")
    def __iter__(self) -> int:
        yield self.degrees
        yield from self.parts

    def __truediv__(self, divisor):
        if isinstance(divisor, Degrees):
            numerator, denominator = 0, 0
            for a, b in zip_longest(
             [self.degrees, *self.parts], [divisor.degrees, *divisor.parts],
             fillvalue=0):
                numerator = numerator * PARTS_IN_DEGREE + a
                denominator = denominator * PARTS_IN_DEGREE + b
            return numerator / denominator
        else:
            return type(self)(*[x / divisor for x in self], 0)

    def __eq__(self, other) -> bool:
        if self.degrees == other.degrees and self.parts[0] == other.parts[0]:
            if round(self.parts[1]) == round(other.parts[1]):
                return True
            elif (self.parts[1] - other.parts[1] == 1 and 
                 (len(self.parts) < 3 or self.parts[2] < 30) and
                 (len(other.parts) >= 3 and other.parts[2] >= 30)):
                return True
            elif (other.parts[1] - self.parts[1] == 1 and 
                 (len(other.parts) < 3 or other.parts[2] < 30) and
                 (len(self.parts) >= 3 and self.parts[2] >= 30)):
                return True
        else:
            return False

    def __round__(self) -> int:
        if self.parts[0] < 30:
            return self.degrees
        else:
            return self.degrees + 1

class DegreesOfCircle(Degrees):
    def reduce(self):
        super().reduce()
        self.degrees %= DEGREES_IN_CIRCLE