""" giorgi - units

This module contains the unit class.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

from typing import Optional, Self

from giorgi.prefices import DECIMAL_PREFICES, UNARY_PREFIX, Prefix
from giorgi.shared import exponent_superscript


class Unit:
    """A class representing units."""

    @staticmethod
    def create_set(*args, scale, prefices: list[Prefix] = DECIMAL_PREFICES, main_prefix: Prefix = UNARY_PREFIX, **kwargs) -> Self:
        """Create a set of units with different prefices."""
        return {prefix: Unit(*args, scale=scale/main_prefix.scale, prefix=prefix, **kwargs) for prefix in prefices}[main_prefix]
        
    def __init__(self,
            quantity: 'Quantity',
            symbol: str,
            scale: float = 1.0,
            *,
            name: Optional[str] = None,
            prefix: Prefix = UNARY_PREFIX,
            no_space_before_unit = False,
            bias: float = 0.0,
        ):
        """Creates a unit for the given quantity.

        -quantity:              the quantity for this unit
        -symbol:                the symbol for this unit
        -scale:                 the scale for this unit, relative to the SI unit for the given quantity
        -name:                  the name for the unit, optional  
        -prefix:                the prefix to be added to the name, symbol and scale 
        -no_space_before_unit:  if True, no space is required before the unit
        -bias:                  used when the unit has a shifted 0 point  
        """
        self.quantity = quantity
        self.symbol = f"{prefix.symbol}{symbol}"
        self.scale = scale*prefix.scale
        self.name = None if name is None else f"{prefix.name}{name}"
        self.no_space_before_unit = no_space_before_unit
        self.bias = bias
        self.quantity._add_unit(self)

    def from_main_unit(self, value: float) -> float:
        """Return the value given in the main unit in this unit."""
        return value/self.scale - self.bias

    def to_main_unit(self, value: float) -> float:
        """Return the value given in this unit in the main unit."""
        return (value + self.bias)*self.scale  
        
    def __eq__(self, other: Self) -> bool:
        """Return whether the given unit is the same as this unit."""
        return self.quantity == other.quantity and self.symbol == other.symbol and self.scale == other.scale and self.bias == other.bias
    
    def __repr__(self) -> str:
        """Return a representation of this unit."""
        return f"Unit('{self.quantity}', '{self.symbol}', scale={self.scale}, bias={self.bias})"
    
    def __str__(self) -> str:
        """Return the symbol of this unit."""
        return self.symbol
    
    # def __invert__(self) -> Self:
    #     """Return a unit that is theinversion of this unit."""
    #     quantity = 1/self.quantity
    #     symbol = f"{self.symbol}{exponent_superscript(-1)}"
    #     scale = 1/self.scale
    #     return Unit(quantity=quantity, symbol=symbol, scale=scale)
    
    def __mul__(self, other: Self) -> Self:
        """Return a unit that is the multiplication of this unit and the given unit."""
        quantity = self.quantity*other.quantity
        symbol = f"{self.symbol}×{other.symbol}"
        scale = self.scale*other.scale
        return Unit(quantity=quantity, symbol=symbol, scale=scale)
    
    def __truediv__(self, other: Self) -> Self:
        """Return a unit that is the division of this unit and the given unit."""
        quantity = self.quantity/other.quantity
        if '×' in other.symbol or '/' in other.symbol:
            symbol = f"{self.symbol}/({other.symbol})"
        else:
            symbol = f"{self.symbol}/{other.symbol}"
        scale = self.scale/other.scale
        return Unit(quantity=quantity, symbol=symbol, scale=scale)
