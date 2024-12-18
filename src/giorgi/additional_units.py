""" giorgi - additional units

This module creates units that are not part of the SI system.

To be completed.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

import math
from giorgi.units import Unit
from .base_quantities import Length, Time, Mass, Temperature, Current, Amount, Luminosity, PlainAngle
from .derived_quantities import Ratio, Area, Volume, Pressure, Conductance


# Geometric quantities
Unit(quantity=Ratio, symbol='%', scale=1e-2, name='percent')
Unit(quantity=Ratio, symbol='‰', scale=1e-3, name='permille')
Unit(quantity=Length, symbol='Å', scale=1e-10, name='ångström')
Unit(quantity=Area, symbol='a', scale=1e2, name='are')
Unit(quantity=Area, symbol='ha', scale=1e4, name='hectare')
Unit(quantity=Area, symbol='ca', scale=1e0, name='centiare')
Unit(quantity=Area, symbol='a', scale=1e2, name='are')
Unit.create(quantity=Volume, symbol='l', scale=1e-3, name='litre')


# Time
Unit(quantity=Time, symbol='min', scale=60, name='minute')
Unit(quantity=Time, symbol='h', scale=60*60, name='hour')
Unit(quantity=Time, symbol='d', scale=60*60*24, name='day')


# Mechanical quantities
Unit(quantity=Pressure, symbol='bar', scale=1e5, name='bar')
Unit(quantity=Pressure, symbol='atm', scale=1.01325e5, name='atmosphere')
Unit(quantity=Pressure, symbol='psi', scale=6894.757, name='pound-force per square inch')


# Electrical quantities
Unit(quantity=Conductance, symbol='℧', scale=1, name='mho')


# Angles
Unit(quantity=PlainAngle, symbol='°', scale=2*math.pi/360, name='degree')
Unit(quantity=PlainAngle, symbol="'", scale=2*math.pi/360/60, name='minute')
Unit(quantity=PlainAngle, symbol='"', scale=2*math.pi/360/60/60, name='second')
