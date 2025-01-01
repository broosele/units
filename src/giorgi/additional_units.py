""" giorgi - additional units

This module creates additional units.

To be completed.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""

import math
from giorgi.prefices import BINARY_PREFICES, DECIMAL_PREFICES
from giorgi.units import Unit
from .base_quantities import Length, Time, Mass, Temperature, Information, PlainAngle
from .derived_quantities import Area, Volume, Pressure, Energy, Conductance


# Geometric quantities
#length
Unit(quantity=Length, symbol='Å', scale=1e-10, name='ångström')
Unit(quantity=Length, symbol='ly', scale=9460730472580800, name='light-year')
foot = 0.3048
Unit(quantity=Length, symbol='twip', scale=foot/17280, name='twip')
Unit(quantity=Length, symbol='th', scale=foot/12000, name='thou')
Unit(quantity=Length, symbol='barleycorn', scale=foot/36, name='barleycorn')
Unit(quantity=Length, symbol='"', scale=foot/12, name='inch')
Unit(quantity=Length, symbol='hh', scale=foot/3, name='hand')
Unit(quantity=Length, symbol="'", scale=foot, name='foot')
Unit(quantity=Length, symbol='yd', scale=foot*3, name='yard')
Unit(quantity=Length, symbol='ch', scale=foot*66, name='chain')
Unit(quantity=Length, symbol='fur', scale=foot*660, name='furlong')
Unit(quantity=Length, symbol='mi', scale=foot*5280, name='mile')
Unit(quantity=Length, symbol='lea', scale=foot*15840, name='league')
#area
[Unit(quantity=Area, symbol=f'{prefix.symbol}m²', scale=prefix.scale**2, name=f'square {prefix.name} metre') for prefix in DECIMAL_PREFICES if prefix.scale != 1]
Unit(quantity=Area, symbol='a', scale=1e2, name='are')
Unit(quantity=Area, symbol='ha', scale=1e4, name='hectare')
Unit(quantity=Area, symbol='ca', scale=1e0, name='centiare')
Unit(quantity=Area, symbol='a', scale=1e2, name='are')
acre = 4046.8564224
Unit(quantity=Area, symbol='ro', scale=acre/4, name='rood')
Unit(quantity=Area, symbol='ac', scale=acre, name='acre')
Unit(quantity=Area, symbol='sq mi', scale=acre*640, name='square mile')
#volume
[Unit(quantity=Area, symbol=f'{prefix.symbol}m³', scale=prefix.scale**3, name=f'cubic {prefix.name} metre') for prefix in DECIMAL_PREFICES if prefix.scale != 1]
Unit.create_set(quantity=Volume, symbol='l', scale=1e-3, name='litre')
fluid_ounce = 28.4130625e-6
Unit(quantity=Volume, symbol='fl oz', scale=fluid_ounce, name='fluid ounce')
Unit(quantity=Volume, symbol='gi', scale=fluid_ounce*5, name='gill')
Unit(quantity=Volume, symbol='pt', scale=fluid_ounce*20, name='pint')
Unit(quantity=Volume, symbol='qt', scale=fluid_ounce*40, name='quart')
Unit(quantity=Volume, symbol='gal', scale=fluid_ounce*160, name='gallon')


# Time
Unit(quantity=Time, symbol='min', scale=60, name='minute')
Unit(quantity=Time, symbol='h', scale=60*60, name='hour')
Unit(quantity=Time, symbol='d', scale=60*60*24, name='day')


# Mass
Unit(quantity=Mass, symbol='t', scale=1e3, name='tonne')
Unit(quantity=Mass, symbol='Da', scale=1.66e-27, name='dalton')
Unit(quantity=Mass, symbol='M☉', scale=1.99e30, name='solar mass')
Unit(quantity=Mass, symbol='Da', scale=1.66e-27, name='dalton')
pound = 0.45359237
Unit(quantity=Mass, symbol='gr', scale=pound/7000, name='grain')
Unit(quantity=Mass, symbol='dr', scale=pound/256, name='drachm')
Unit(quantity=Mass, symbol='oz', scale=pound/16, name='ounce')
Unit(quantity=Mass, symbol='lb', scale=pound, name='pound')
Unit(quantity=Mass, symbol='st', scale=pound*14, name='stone')
Unit(quantity=Mass, symbol='qr', scale=pound*28, name='quarter')
Unit(quantity=Mass, symbol='cwt', scale=pound*112, name='hundredweight')
Unit(quantity=Mass, symbol='long ton', scale=pound*2240, name='long ton')
Unit(quantity=Mass, symbol='short ton', scale=pound*2000, name='short ton')
Unit(quantity=Mass, symbol='slug', scale=14.59390294, name='slug')

# Temperature
Unit(quantity=Temperature, symbol='°C', scale=1, bias=273.15, name='celsius')
Unit(quantity=Temperature, symbol='°F', scale=5/9, bias=459.67, name='fahrenheit')
Unit(quantity=Temperature, symbol='°R', scale=5/9, name='rankine')


# Mechanical quantities
Unit.create_set(quantity=Pressure, symbol='bar', scale=1e5, name='bar')
Unit(quantity=Pressure, symbol='atm', scale=1.01325e5, name='atmosphere')
Unit(quantity=Pressure, symbol='psi', scale=6894.757, name='pound-force per square inch')
Unit(quantity=Energy, symbol='Wh', scale=3600, name='watt-hour')
Unit.create_set(quantity=Energy, symbol='eV', scale=1.602176634e-19, name='electron-volt')


# Electrical quantities
Unit(quantity=Conductance, symbol='℧', scale=1, name='mho')


# Information
Unit.create_set(quantity=Information, symbol='B', scale=8, name='byte', prefices=BINARY_PREFICES + DECIMAL_PREFICES)
Unit(quantity=Information, symbol='nibble', scale=4, name='nibble')


# Angles
Unit(quantity=PlainAngle, symbol='°', scale=2*math.pi/360, name='degree', no_space_before_unit=True)
Unit(quantity=PlainAngle, symbol="'", scale=2*math.pi/360/60, name='minute', no_space_before_unit=True)
Unit(quantity=PlainAngle, symbol='"', scale=2*math.pi/360/60/60, name='second', no_space_before_unit=True)
