""" giorgi - base quantities

This module creates the base quantities:
- physical quantities of the SI system
- information
- angles

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

from giorgi.prefices import BINARY_PREFICES, DECIMAL_PREFICES, DECIMAL_PREFIX_BY_EXPONENT
from giorgi.quantities import BaseQuantityType


# Physical SI base quantities
Length = BaseQuantityType('Length', unit_symbol='m', unit_name='metre')
Time = BaseQuantityType('Time', unit_symbol='s', unit_name='second')
Mass = BaseQuantityType('Mass', unit_symbol='g', unit_name='gram', main_unit_prefix=DECIMAL_PREFIX_BY_EXPONENT[3])
Temperature = BaseQuantityType('Temperature', unit_symbol='K', unit_name='kelvin')
Current = BaseQuantityType('Current', unit_symbol='A', unit_name='ampere')
Amount = BaseQuantityType('Amount', unit_symbol='mol', unit_name='mole')
LuminousIntensity = BaseQuantityType('Luminous intensity', unit_symbol='Cd', unit_name='candela')


# Unit of information
Information = BaseQuantityType('Information', unit_symbol='b', unit_name='bit', prefices=BINARY_PREFICES + DECIMAL_PREFICES)


# Angles
PlainAngle = BaseQuantityType('Plain angle', unit_symbol='rad', unit_name='radian')
SolidAngle = BaseQuantityType('Solid angle', unit_symbol='sr', unit_name='steradian')
