""" giorgi - units

A library to work with units.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

from typing import Optional, Self

from giorgi.prefices import UNARY_PREFIX, Prefix
from giorgi.shared import exponent_superscript


class Unit:

    @staticmethod
    def create(
            quantity: 'Quantity',
            symbol: str,
            prefix: Prefix = UNARY_PREFIX,
            scale: float = 1.0,
            name: Optional[str] = None,
        ) -> Self:
        symbol = f"{prefix.symbol}{symbol}"
        scale = scale*prefix.scale
        name = None if name is None else f"{prefix.name}{name}"
        return Unit(quantity=quantity, symbol=symbol, scale=scale, name=name)

    @staticmethod
    def create_set(
            quantity: 'Quantity',
            symbol: str,
            prefices: list[Prefix],
            main_prefix: Prefix = UNARY_PREFIX,
            name: Optional[str] = None,
        ) -> Self:
        scale = 1/main_prefix.scale
        return {prefix: Unit.create(quantity=quantity, symbol=symbol, prefix=prefix, scale=scale, name=name) for prefix in prefices}[main_prefix]
        
    def __init__(self,
            quantity: 'Quantity',
            symbol: str,
            scale: float = 1.0,
            name: Optional[str] = None,
        ):
        """Creates a unit for the given quantity.

        -quantity:  the quantity for this unit
        -symbol:    the symbol for this unit
        -scale:     the scale for this unit, relative to the SI unit for the given quantity
        -name:      the name for the unit, optional     
        """
        self.quantity = quantity
        self.symbol = symbol
        self.scale = scale
        self.name = name
        self.quantity._add_unit(self)
        
    def __eq__(self, other: Self) -> bool:
        return self.quantity == other.quantity and self.symbol == other.symbol and self.scale == other.scale
    
    def __str__(self) -> str:
        return self.symbol
    
    def __invert__(self) -> Self:
        quantity = 1/self.quantity
        symbol = f"{self.symbol}{exponent_superscript(-1)}"
        scale = 1/self.scale
        return Unit(quantity=quantity, symbol=symbol, scale=scale)
    
    def __mul__(self, other: Self) -> Self:
        quantity = self.quantity*other.quantity
        symbol = f"{self.symbol}×{other.symbol}"
        scale = self.scale*other.scale
        return Unit(quantity=quantity, symbol=symbol, scale=scale)
    
    def __truediv__(self, other: Self) -> Self:
        quantity = self.quantity/other.quantity
        if '×' in other.symbol or '/' in other.symbol:
            symbol = f"{self.symbol}/({other.symbol})"
        else:
            symbol = f"{self.symbol}/{other.symbol}"
        scale = self.scale/other.scale
        return Unit(quantity=quantity, symbol=symbol, scale=scale)
