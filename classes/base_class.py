from abc import ABC
from itertools import zip_longest
from decimal import Decimal


class MeasureWithSubunits(ABC):
    """Base class for a compound unit, made up of subunits.

    The names of the units and subunits, and the number of subunits in each 
    unit or next greater subunit must be given in a dict that is a class 
    variable.
    This must be assigned with the first object of the class type.
    After this has been assigned, it cannot be changed.
    """

    units = {}
    """The names of the units and subunits, and the number of subunits that 
    make up each unit. The unit can be assigned to the number of units in a 
    cycle.
    """

    cycle = False
    """Class setting, whether to constrict the basic unit in a repeating cycle 
    or not. """

    child_class = None
    """Used for division. Must be assigned after the child class has 
    been defined."""

    strict = True
    """If true, an equality comparison between this type any other returns 
    false and greater or less than comparisons raises a TypeError"""
    
    def __init__(self, *args, units: dict = None) -> None:
        #ensure units are defined
        if units is not None and units != self.units:
            if self.units == {}:
                type(self).units = units
            else:
                raise ValueError('Cannot reasign units')
        if self.units == {}:
            raise ValueError('Must supply unit mapping')
        #assign vars for processing
        self.__dict__['unit_list'] = tuple(self.units.keys())
        subunits = tuple(self.units.values())
        measures = [args[i] if i < len(args) else 0
                    for i in range(len(self.unit_list))]
        #reduce
        carry = 0
        for i in range(len(self.unit_list)):
            measures[i] += carry * subunits[i]
            measures[i], carry = divmod(measures[i], 1)
        carry = 0
        for i in range(-1, -len(self.unit_list), -1):
            measures[i] += carry
            carry, measures[i] = divmod(measures[i], subunits[i])
        measures[0] += carry
        if self.cycle and measures[0] != 0:
            measures[0] %= subunits[0]
        #assign
        for unit, measure in zip(self.unit_list, measures):
            self.__dict__[unit] = int(measure)
    
    def __getitem__(self, index) -> int:
        if type(index) is int:
            return self.__dict__[self.unit_list[index]]
        elif type(index) is slice:
            return [self.__dict__[self.unit_list[i]] for i in range(
                    index.start or 0,
                    index.stop or len(self.unit_list),
                    index.step or 1
                   )]
        else:
            return self.__dict__[index]

    def __len__(self) -> int:
        return len(self.unit_list)

    def __repr__(self) -> str:
        measures = ', '.join(str(num) for num in self)
        return f'{self.__class__.__name__}({measures}, units={self.units})'

    def __str__(self) -> str:
        """Should be overwritten with unit-specific formatting"""
        return '(' + ', '.join(str(num) for num in self) + ')'
 
    def __setattr__(self, name, attr_value):
        raise AttributeError(f"'{self.__class__.__name__}' "
            "object does not support attribute assignment")

    def __hash__(self) -> int:
        return hash(tuple(self))
    
    # comparison functions
    def __eq__(self, other) -> bool:
        if self.strict and not isinstance(other, self.__class__):
            return False
        for x, y in zip_longest(self, other, fillvalue=0):
            if x == y:
                continue
            else:
                return False
        return True

    def __gt__(self, other) -> bool:
        if self.strict and not isinstance(other, self.__class__):
            raise TypeError("'>' not supported between instances of "
                f"'{self.__class__.__name__}' and "
                f"'{other.__class__.__name__}'")
        for x, y in zip_longest(self, other, fillvalue=0):
            if   x >  y:
                return True
            elif x == y:
                continue
            else: # x < y
                return False
        # if x == y for all
        return False

    def __lt__(self, other) -> bool:
        if self.strict and not isinstance(other, self.__class__):
            raise TypeError("'<' not supported between instances of "
                f"'{self.__class__.__name__}' and "
                f"'{other.__class__.__name__}'")
        for x, y in zip_longest(self, other, fillvalue=0):
            if   x <  y:
                return True
            elif x == y:
                continue          
            else: # x > y
                return False
        # if x == y for all
        return False

    def __ge__(self, other) -> bool:
        return self > other or self == other
    def __le__(self, other) -> bool:
        return self < other or self == other

    # math functions
    def __add__(self, addend):
        if self.strict and not isinstance(addend, self.__class__):
            raise TypeError("'+' not supported between instances of "
                f"'{self.__class__.__name__}' and "
                f"'{addend.__class__.__name__}'")
        return type(self)(*[x + y
         for x, y in zip_longest(self, addend, fillvalue=0)])
    def __radd__(self, addend):
        return self + addend

    def __sub__(self, subtrahend):
        if self.strict and not isinstance(subtrahend, self.__class__):
            raise TypeError("'-' not supported between instances of "
                f"'{self.__class__.__name__}' and "
                f"'{subtrahend.__class__.__name__}'")
        return type(self)(*[x - y 
         for x, y in zip_longest(self, subtrahend, fillvalue=0)])

    def __mul__(self, factor):
        return type(self)(*[x * factor for x in self])
    def __rmul__(self, factor):
        return self * factor
    def __floordiv__(self, divisor):
        return type(self)(*[x / divisor for x in self])

    def __truediv__(self, divisor):
        if isinstance(divisor, self.__class__):
            # Ratio
            numerator, denominator = 0, 0
            for a, b, unit in zip(self, divisor, self.units):
                numerator = numerator * self.units[unit] + a
                denominator = denominator * self.units[unit] + b
            return numerator / denominator
        elif self.child_class:
            # scaller division resulting in measure with additional subunit
            div_dec = Decimal(divisor)
            return self.child_class(*[x / div_dec for x in self], 0)
        else:
            raise TypeError("Division is not supported for type "
                f"'{type(divisor)}'")
            
    def __neg__(self):
        return self * -1
    def __abs__(self):
        return -self if self < type(self)(0) else self
    def __round__(self) -> int:
        return ( self[0]
            if   self[1] < self.units[self.unit_list[1]] / 2
            else self[0] + 1)
