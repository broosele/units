""" giorgi - quantities

This module contains the metaclass for quantity types as well as the base class for those quantities.

<some explanation is needed here>

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

from functools import reduce
import math
from typing import Optional, Self, TypeVar

from giorgi.prefices import DECIMAL_PREFICES, UNARY_PREFIX, Prefix
from giorgi.shared import exponent_superscript
from giorgi.units import Unit


QUANTITYTYPE = TypeVar('Quantity') | int | float
"""A type variable to descibes the type which is considered a quantity,
including dimensionless quantities which are represented by numerical values."""


class Quantity:
    """Abstract class for quantities.
    
    A quantity is an amount of something.
    E.g. 5 metres, 10 seconds

    It can be expressed in different units. This unit is not part of the quantity.
    Internally, the value of a quantity is expressed in the main unit set by the Quantity type.

    Quantities are immutable instances.

    The value can be set in different ways:
    * with a single positional argument, in this case the main unit is used:
        Mass(1) -> 1.000 kg
    * with two positional arguments, in this case the unit can be chosen:
        Mass(1, 'g') -> 0.001 kg
        Mass(3, 'gram') -> 0.003 kg
    * with keyword arguments, in this case the name/value pairs represent unit and value.
        Multiple values can be given, the resulting values are weighted and added:
        Time(h=1, min=3, s=5) -> 3785.000 s
    * the two methods can be combined.
    """
    def __init__(self, value=0, symbol_or_name=None, **kwargs):
        self.value = self.unit(symbol_or_name).to_main_unit(value) + \
            sum(self.unit(symbol_or_name).to_main_unit(value) for symbol_or_name, value in kwargs.items())

    @classmethod
    def unit(cls, name_or_symbol) -> Unit:
        """Return the Unit instance for this quantity type with the given name of symbol."""
        if name_or_symbol is None:
            return cls.main_unit
        return cls._units[name_or_symbol]
    
    def in_unit(self, symbol_or_name) -> float:
        """Return the value of this quantity expressed in the unit with the given name or symbol."""
        return self.unit(symbol_or_name).from_main_unit(self.value)

    def __hash__(self):
        return hash((self.value, type(self)))
    
    def to_string(self, unit: Unit, float_fmt: str='.6f') -> str:
        """Return a string representation of this value, in the given unit an with the given float format.
        
        The float format is as defined by the formatting mini-language:
        (https://docs.python.org/3/library/string.html#formatspec)
        """
        return f"{unit.from_main_unit(self.value):{float_fmt}}{'' if unit.no_space_before_unit else ' '}{unit.symbol}"

    def __repr__(self) -> str:
        """Return a representation of this quantity."""
        return f"{type(self).__name__}({self.value})"
    
    def __str__(self) -> str:
        """Return a readable representation of this quantity."""
        return self.to_string(unit=self.main_unit, float_fmt='.3f')
    
    def __format__(self, fmt: str) -> str:
        """Implements the formatting protocol.
        
        The format string can be any format string used for floats with optionally a unit symbol added.
        E.g.
        f"{Mass(1):8.5g}" -> '  1000.0 g'
        """
        for unit_symbol in sorted(self._units, key=lambda symbol: -len(symbol)):
            if fmt.endswith(unit_symbol):
                unit = self.unit(unit_symbol)
                float_fmt = fmt[:-len(unit_symbol)]
                break
        else:
            unit = self.main_unit
            float_fmt = fmt
        return self.to_string(unit=unit, float_fmt=float_fmt)
    
    def __neg__(self) -> Self:
        """Return a quantity representing negative of this quantity."""
        return type(self)(-self.value)
    
    def __add__(self, other: Self) -> Self:
        """Return a quantity that represents the sum of this an the other quantity.
        
        Only quantities of the same type can be added.
        """
        if type(self) != type(other):
            raise TypeError("Can only add quantities of same type together")
        return type(self)(self.value + other.value)

    
    def __sub__(self, other: Self) -> Self:
        """Return a quantity that represents the difference between this an the other quantity.
        
        Only quantities of the same type can be subtracted.
        """
        return self + -other
    
    def __mul__(self, other: QUANTITYTYPE) -> QUANTITYTYPE:
        """Return a quantity (or numerical value) that represents the multiplication of this and
        the other quantity or numerical value.
        """
        if isinstance(other, (int, float)):
            return type(self)(self.value*other)
        else:
            return (type(self)*type(other))(self.value*other.value)
    
    def __rmul__(self, other: int | float) -> Self:
        """Return a quantity that represents the multiplication of this quantity and a numerical value."""
        return self*other
    
    def __truediv__(self, other: QUANTITYTYPE) -> QUANTITYTYPE:
        """Return a quantity (or numerical value) that represents the division of this and
        the other quantity or numerical value.
        """
        if isinstance(other, (int, float)):
            return type(self)(self.value/other)
        else:
            return (type(self)/type(other))(self.value/other.value)
    
    def __rtruediv__(self, other: int | float) -> Self:
        """Return a quantity that represents the division of this quantity and a numerical value."""        
        if isinstance(other, (int, float)):
            return (1/type(self))(other/self.value)
        else:
            raise TypeError()
    
    def __floordiv__(self, other: Self) -> int:
        """Return an int that represents the integer division of this quantity and another quantity of the same type."""  
        if type(self) != type(other):
            raise TypeError()
        return self.value//other.value
    
    def __mod__(self, other: Self) -> Self:
        """Return a quantity that represents the modulo remainer of this quantity another quantity of the same type."""        
        if type(self) != type(other):
            raise TypeError()
        return (type(self)/type(other))(self.value%other.value)
    
    def __divmod__(self, other: Self) -> tuple[float, Self]:
        """Return a tuple of an int and a quantity of the same type that represents a integer quotient and remainder."""
        if type(self) != type(other):
            raise TypeError()
        return self//other, self%other
    
    def __pow__(self, exponent: int):
        """Return a quantity that is a integer power of this quantity."""
        return reduce(Quantity.__mul__, [self]*exponent)
    
    def __eq__(self, other: Self) -> bool:
        """Return whether this quantity is equal to the given quantity. Small numerical inaccuracies are ignored."""
        if type(self) != type(other):
            raise TypeError()
        return math.isclose(self.value, other.value)
    
    def __lt__(self, other: Self) -> bool:
        """Return whether this quantity is smaller than the given quantity."""
        if type(self) != type(other):
            raise TypeError()
        return self.value < other.value and self != other
    
    def __le__(self, other: Self) -> bool:
        """Return whether this quantity is smaller than or equal to the given quantity."""
        if type(self) != type(other):
            raise TypeError()
        return self.value <= other.value or self == other
    
    def __gt__(self, other: Self) -> bool:
        """Return whether this quantity is bigger than the given quantity."""
        if type(self) != type(other):
            raise TypeError()
        return self.value > other.value and self != other
    
    def __ge__(self, other: Self) -> bool:
        """Return whether this quantity is bigger than or equal to the given quantity."""
        if type(self) != type(other):
            raise TypeError()
        return self.value >= other.value or self == other
    
    
class QuantityType(type):
    """The type for quantity types.
    
    This is a metaclass, not a class to be inherited from.

    Instances of this metaclass (quantity types) can be dynamically created.
    """

    _existing: dict[tuple[tuple['BaseQuantity', int], ...], Self] = dict()
    """A dictionary containing existing quantity types. Keys are the expansion in base quantities."""
    
    @staticmethod
    def _hashable_base_quantities(base_quantities: dict['BaseQuantity', int]) -> tuple[tuple['BaseQuantity', int], ...]:
        """Return a hashable form of the expansion in base quantities."""
        return tuple(
            (base_quantity, exponent)
                for base_quantity, exponent in sorted(base_quantities.items(), key=lambda kv: str(kv[0]))
                if exponent
        )
    
    def __new__(cls, name, base_quantities: dict['BaseQuantity', int], *args, **kwargs) -> Self:
        """Ensures all quantity types instances inherit from Quantity."""
        return super().__new__(cls, name, (Quantity,), {})

    @staticmethod
    def get_quantity_type(base_quantities: dict['BaseQuantity', int]) -> float | Self:
        """Return a quantity type with the given expansion in base types.
        
        If such a type already exists, it is returned, otherwise a new one is dynamically created.
        
        Whenever quantity types are created as local variables, this method should be used.

        Types that are created this way have generic names and units as defined in __init__.        
        """
        if all(v == 0 for v in base_quantities.values()):
            return float
        base_quantities = {k: v for k, v in base_quantities.items() if v}
        hashable_base_quantities = QuantityType._hashable_base_quantities(base_quantities)
        try:
            return QuantityType._existing[hashable_base_quantities]
        except KeyError:
            name = ''.join(f"{base_quantity}{exponent}" for base_quantity, exponent in hashable_base_quantities)
            return QuantityType(name, base_quantities)
    
    def __init__(self,
            name: str,
            base_quantities: dict['BaseQuantity', int],
            unit_symbol: Optional[str] = None,
            unit_name: Optional[str] = None,
            main_unit_prefix: Prefix = UNARY_PREFIX,
            prefices: list[Prefix] = DECIMAL_PREFICES,
        ):
        """Create a new quantity type.
            
        Arguments:
            name: the name of the quantity type (class name), e.g. 'Force'
            base_quantities: a dict mapping base quantities on their power, e.g. {'Length': 1, Time: -2, Mass: 1} means force
            unit_symbol: the symbol of the unit specific for the quantity type, if it exists, e.g. 'N'
            unit_name: the full name of the unit, e.g. 'Newton'
            main_unit_prefix: the prefix (string) used together with the unit symbol for the 'main' unit. Normally this is '', but can be different (kg)
            prefices: a list of prefices. These will be used to create additional units for the quantity type
        
        If a quantity type with the same expansion in base quantities already exists, an error is raised. Use 'get_quantity_type' to avoid this.
        """
        self.name = name
        self.base_quantities = base_quantities        
        hashable_base_quantities = QuantityType._hashable_base_quantities(base_quantities)
        self._units = {}
        if unit_symbol is None:
            unit_symbol = '×'.join(f"{base_quantity.main_unit.symbol}{exponent_superscript(exponent)}" for base_quantity, exponent in hashable_base_quantities)
            unit_scale = reduce(lambda a, b: a*b, (base_quantity.main_unit.scale**exponent for base_quantity, exponent in hashable_base_quantities))
            self.main_unit = Unit(self, symbol=unit_symbol, scale=unit_scale)
        else:
            self.main_unit = Unit.create_set(self, symbol=unit_symbol, scale=1, prefices=prefices, main_prefix=main_unit_prefix, name=unit_name)
        if self.main_unit.scale != 1 or self.main_unit.bias != 0:
            raise ValueError("Main units should have scale 1 and bias 0.")
        hashable_base_quantities = QuantityType._hashable_base_quantities(base_quantities)
        if hashable_base_quantities in QuantityType._existing:
            raise ValueError(f"Quantity type with base quantities {base_quantities} already exists.")
        else:
            QuantityType._existing[hashable_base_quantities] = self

    def __hash__(self):
        return hash(QuantityType._hashable_base_quantities(self.base_quantities))
    
    def __repr__(self) -> str:
        """Return a representation of this quantity type."""
        return f"QuantityType('{self}')"
    
    def __str__(self) -> str:
        """Return the type name."""
        return self.__name__
    
    def __getitem__(self, base_quantity: 'BaseQuantity') -> int:
        """Return the exponent of the given base quantity in the expansion of this quantity type."""
        return self.base_quantities.get(base_quantity, 0)
    
    def __mul__(self, other: Self) -> Self:
        """Return the quantity type that is the multiplication of this and the given quantity type."""
        base_quantities = {base_quantity: self[base_quantity] + other[base_quantity] for base_quantity in set(self.base_quantities)|set(other.base_quantities)}
        return QuantityType.get_quantity_type(base_quantities=base_quantities)
    
    def __truediv__(self, other: Self) -> Self:
        """Return the quantity type that is the division of this and the given quantity type."""
        base_quantities = {base_quantity: self[base_quantity] - other[base_quantity] for base_quantity in set(self.base_quantities)|set(other.base_quantities)}
        return QuantityType.get_quantity_type(base_quantities=base_quantities)
    
    def __rtruediv__(self, other: 1) -> Self:
        """Return the quantity type that is the inverse of this quantity type (other should be 1)."""
        if not isinstance(other, (float, int)) or other != 1:
            raise ValueError()
        base_quantities = {base_quantity: -self[base_quantity] for base_quantity in self.base_quantities}
        return QuantityType.get_quantity_type(base_quantities=base_quantities)
    
    def __pow__(self, exponent: int) -> Self:
        """Return the quantity type that is this quantity type raised to the given (integer) power."""
        base_quantities = {base_quantity: self[base_quantity]*exponent for base_quantity in self.base_quantities}
        return QuantityType.get_quantity_type(base_quantities=base_quantities)
    
    def __eq__(self, other: Self) -> bool:
        """Return whether the given quantity type is the same as this quantity type."""
        return self is other

    def _add_unit(self, unit: Unit):
        """Add the given unit to the list of available units for this quantity type."""
        self._units[unit.symbol] = unit
        if unit.name:
            self._units[unit.name.replace(' ', '_')] = unit


class BaseQuantityType(QuantityType):
    """Base quantities types are quantity types that cannot be expanded, they form the base of the quantity system.
    
    For physical quantities, these are based on the SI system and are all predefined.

    In addition, base quantities are defined for plain and solid angles and for information.

    Each currency is defined as its own base quantity.
    """
        
    def __new__(cls, name: str, **kwargs):
        return super().__new__(cls, name, None, **kwargs)

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, {self: 1},  *args, **kwargs)

    def __hash__(self):
        return hash(self.__name__)
