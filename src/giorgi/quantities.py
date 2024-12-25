
""" giorgi - quantities

This module the metaclass for quantity types as well as the base class for those quantities.

<some explanation is needed here>

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

from functools import reduce
import math
import re
from typing import Optional, Self

from giorgi.prefices import DECIMAL_PREFICES, DECIMAL_PREFIX_BY_EXPONENT, Prefix
from giorgi.shared import exponent_superscript
from giorgi.units import Unit


class Quantity:
    
    def __init__(self, value=0, symbol_or_name=None, **kwargs):
        self.value = self.unit(symbol_or_name).to_main_unit(value) + \
            sum(self.unit(symbol_or_name).to_main_unit(value) for symbol_or_name, value in kwargs.items())

    @classmethod
    def unit(cls, name_or_symbol):
        if name_or_symbol is None:
            return cls.main_unit
        return cls._units[name_or_symbol]

    def __hash__(self):
        return hash((self.value, type(self)))
    
    def to_string(self, unit: Unit, float_fmt: str='.6f') -> str:
        return f"{unit.from_main_unit(self.value):{float_fmt}}{'' if unit.no_space_before_unit else ' '}{unit.symbol}"

    def __repr__(self) -> str:
        return self.to_string(unit=self.main_unit)
    
    def __str__(self) -> str:
        return self.to_string(unit=self.main_unit, float_fmt='.3f')
    
    def __format__(self, fmt: str) -> str:
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
        return type(self)(-self.value)
    
    def __add__(self, other: Self) -> Self:
        if other == 0:
            return self
        if type(self) != type(other):
            raise TypeError("Can only add quantities of same type together")
        return type(self)(self.value + other.value)
    
    def __radd__(self, other: Self) -> Self:
        return self + other
    
    def __sub__(self, other: Self) -> Self:
        return self + -other
    
    def __rsub__(self, other: Self) -> Self:
        return other + -self
    
    def __mul__(self, other: int | float | Self) -> Self:
        if isinstance(other, (int, float)):
            return type(self)(self.value*other)
        else:
            return (type(self)*type(other))(self.value*other.value)
    
    def __rmul__(self, other: int | float) -> Self:
        return self*other
    
    def __truediv__(self, other: int | float | Self) -> Self:
        if isinstance(other, (int, float)):
            return type(self)(self.value/other)
        else:
            return (type(self)/type(other))(self.value/other.value)
    
    def __rtruediv__(self, other: int | float) -> Self:
        if not isinstance(other, (int, float)):
            raise TypeError()
        return other/self
    
    def __div__(self, other: int | float | Self) -> Self:
        if type(self) != type(other):
            raise TypeError()
        return (type(self)/type(other))(self.value//other.value)
    
    def __pow__(self, exponent: int):
        return reduce(Quantity.__mul__, [self]*exponent)
    
    def __eq__(self, other: Self) -> bool:
        if type(self) != type(other):
            raise TypeError()
        return math.isclose(self.value, other.value)
    
    def __lt__(self, other: Self) -> bool:
        if type(self) != type(other):
            raise TypeError()
        return self.value < other.value and self != other
    
    def __le__(self, other: Self) -> bool:
        if type(self) != type(other):
            raise TypeError()
        return self.value <= other.value or self == other
    
    def __gt__(self, other: Self) -> bool:
        if type(self) != type(other):
            raise TypeError()
        return self.value > other.value and self != other
    
    def __ge__(self, other: Self) -> bool:
        if type(self) != type(other):
            raise TypeError()
        return self.value >= other.value or self == other
    
    
class QuantityType(type):

    existing = dict()
    
    @staticmethod
    def _hashable_base_quantities(base_quantities):
        return tuple((base_quantity, exponent) for base_quantity, exponent in sorted(base_quantities.items(), key=lambda kv: str(kv[0])) if exponent)
    
    def __new__(cls, name, base_quantities, *args, **kwargs):
        if base_quantities == {}:
            return float
        return super().__new__(cls, name, (Quantity,), {})

    def make(base_quantities):
        base_quantities = {k: v for k, v in base_quantities.items() if v}
        hashable_base_quantities = QuantityType._hashable_base_quantities(base_quantities)
        try:
            return QuantityType.existing[hashable_base_quantities]
        except KeyError:
            name = ''.join(f"{base_quantity}{exponent}" for base_quantity, exponent in hashable_base_quantities)
            return QuantityType(name, base_quantities)
    
    def __init__(self,
            name: str,
            base_quantities: dict['BaseQuantity', int],
            unit_symbol: Optional[str] = None,
            unit_name: Optional[str] = None,
            main_unit_prefix: Prefix = DECIMAL_PREFIX_BY_EXPONENT[0],
            prefices: list[Prefix] = DECIMAL_PREFICES,
        ):
        self.name = name
        self.base_quantities = base_quantities        
        hashable_base_quantities = QuantityType._hashable_base_quantities(base_quantities)
        self._units = {}
        if unit_symbol is None:
            unit_symbol = '×'.join(f"{base_quantity.main_unit.symbol}{exponent_superscript(exponent)}" for base_quantity, exponent in hashable_base_quantities)
            unit_scale = reduce(lambda a, b: a*b, (base_quantity.main_unit.scale**exponent for base_quantity, exponent in hashable_base_quantities))
            self.main_unit = Unit(self, symbol=unit_symbol, scale=unit_scale)
        else:
            self.main_unit = Unit.create_set(self, symbol=unit_symbol, prefices=prefices, main_prefix=main_unit_prefix, name=unit_name)
        QuantityType.existing[QuantityType._hashable_base_quantities(base_quantities)] = self

    def __hash__(self):
        return hash(QuantityType._hashable_base_quantities(self.base_quantities))
    
    def __str__(self):
        return self.__name__
    
    def __repr__(self):
        return f"QuantityType('{self}')"
    
    def __getitem__(self, base_quantity):
        return self.base_quantities.get(base_quantity, 0)
    
    def __mul__(self, other: Self) -> Self:
        base_quantities = {base_quantity: self[base_quantity] + other[base_quantity] for base_quantity in set(self.base_quantities)|set(other.base_quantities)}
        return QuantityType.make(base_quantities=base_quantities)
    
    def __truediv__(self, other: Self) -> Self:
        base_quantities = {base_quantity: self[base_quantity] - other[base_quantity] for base_quantity in set(self.base_quantities)|set(other.base_quantities)}
        return QuantityType.make(base_quantities=base_quantities)
    
    def __pow__(self, exponent: int):
        base_quantities = {base_quantity: self[base_quantity]*exponent for base_quantity in self.base_quantities}
        return QuantityType.make(base_quantities=base_quantities)
    
    def __eq__(self, other: Self) -> bool:
        return QuantityType._hashable_base_quantities(self.base_quantities) == QuantityType._hashable_base_quantities(other.base_quantities)
    
    def _add_unit(self, unit):
        self._units[unit.symbol] = unit
        if unit.name:
            self._units[unit.name.replace(' ', '_')] = unit


class BaseQuantityType(QuantityType):
        
    def __new__(cls, name, **kwargs):
        return super().__new__(cls, name, None, **kwargs)

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, {self: 1},  *args, **kwargs)

    def __hash__(self):
        return hash(self.__name__)
