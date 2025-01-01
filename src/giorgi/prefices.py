""" giorgi - prefices

A library to use prefices.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

import math
from typing import Self


class Prefix:

    existing: dict[tuple[str, str, float], Self] = {}

    @staticmethod
    def make(name: str, symbol: str, exponent: int, radix: int) -> Self:
        """Create a new Prefix, or if an identical Prefix already exists, return it."""
        scale = radix**exponent
        key = name, symbol, scale
        try:
            return Prefix.existing[key]
        except KeyError:
            Prefix.existing[key] = Prefix(name=name, symbol=symbol, scale=radix**exponent)
            return Prefix.existing[key]


    """A class defining scale prefices.
    
    Name, symbol and scale should all be unique.
    """
    def __init__(self, name: str, symbol: str, scale: int):
        self.name = name
        self.symbol = symbol
        self.scale = scale

    def __hash__(self):
        return hash((self.name, self.symbol, self.scale))

    def is_power_of(self, radix: int) -> bool:
        """Return whether the scale of this prefix is a power of the given radix."""
        return math.log(self.scale, radix).is_integer()
    
    def exponent(self, radix: int) -> float:
        """Return the exponent to which the given radix needs to be raised to get the scale of this prefix."""
        exponent = math.log(self.scale, radix)
        if not math.isclose(exponent, round(exponent)):
            raise ValueError()
        return round(exponent)


DECIMAL_PREFICES: tuple[Prefix] = tuple(Prefix.make(*values, radix=10) for values in [
    ('quetta'   , 'Q'   , 30    ),
    ('ronna'    , 'R'   , 27    ),
    ('yotta'    , 'Y'   , 24    ),
    ('zetta'    , 'Z'   , 21    ),
    ('exa'      , 'E'   , 18    ),
    ('peta'     , 'P'   , 15    ),
    ('tera'     , 'T'   , 12    ),
    ('giga'     , 'G'   , 9     ),
    ('mega'     , 'M'   , 6     ),
    ('myria'    , 'my'  , 4     ),
    ('kilo'     , 'k'   , 3     ),
    ('hecto'    , 'h'   , 2     ),
    ('deca'     , 'da'  , 1     ),
    (''         , ''    , 0     ),
    ('deci'     , 'd'   , -1    ),
    ('centi'    , 'c'   , -2    ),
    ('milli'    , 'm'   , -3    ),
    ('micro'    , 'μ'   , -6    ),
    ('nano'     , 'n'   , -9    ),
    ('pico'     , 'p'   , -12   ),
    ('femto'    , 'f'   , -15   ),
    ('atto'     , 'a'   , -18   ),
    ('zepto'    , 'z'   , -21   ),
    ('yocto'    , 'y'   , -24   ),
    ('ronto'    , 'r'   , -27   ),
    ('quecto'   , 'q'   , -30   ),
])
"""A tuple of existing SI prefices."""


BINARY_PREFICES: tuple[Prefix] = tuple(Prefix.make(*values, radix=2) for values in [
    ('yobi'     , 'Yi'  , 80    ),
    ('zebi'     , 'Zi'  , 70    ),
    ('exbi'     , 'Ei'  , 60    ),
    ('pebi'     , 'Pi'  , 50    ),
    ('tebi'     , 'Ti'  , 40    ),
    ('gibi'     , 'Gi'  , 30    ),
    ('mebi'     , 'Mi'  , 20    ),
    ('kibi'     , 'Ki'  , 10    ),
    (''         , ''    , 0     ),
    
])
"""A tuple of existing binary prefices."""


DECIMAL_PREFIX_BY_EXPONENT: dict[int, Prefix] = {prefix.exponent(10): prefix for prefix in DECIMAL_PREFICES}
"""A mapping of exponents to their corresponding SI prefices."""


BINARY_PREFIX_BY_EXPONENT: dict[int, Prefix] = {prefix.exponent(2): prefix for prefix in BINARY_PREFICES}
"""A mapping of exponents to their corresponding binary prefices."""


UNARY_PREFIX = DECIMAL_PREFIX_BY_EXPONENT[0]
"""The prefix with scale 1."""


def si_prefix(value: float) -> Prefix:
    """A function returning the appropriate SI prefix for a given value."""
    exponent = min(max(3*(math.log10(value)//3), -30), 30)
    return DECIMAL_PREFIX_BY_EXPONENT[exponent]


def binary_prefix(value: float) -> Prefix:
    """A function returning the appropriate binary prefix for a given value."""
    exponent = min(max(10*(math.log2(value)//10), 10), 80)
    return BINARY_PREFIX_BY_EXPONENT[exponent]
