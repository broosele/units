""" giorgi - derived quantities

This module creates the physical derived quantities of the SI system.

To be completed.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""


from giorgi.prefices import UNARY_PREFIX
from giorgi.quantities import QuantityType
from .base_quantities import Length, Time, Mass, Temperature, Current, Amount, Luminosity


# Geometric quantities
# Ratio = QuantityType('Ratio', {}, '', prefices=[UNARY_PREFIX])
Area = QuantityType('Area', {Length: 2})
Volume = QuantityType('Volume', {Length: 3})


# Mechanical quantities
Speed = QuantityType('Speed', {Length: 1, Time: -1})
Acceleration = QuantityType('Acceleration', {Length: 1, Time: -2})
Force = QuantityType('Force', {Mass: 1, Length: 1, Time: -2}, 'N', 'newton')
Pressure = QuantityType('Pressure', {Mass: 1, Length: -1, Time: -2}, 'Pa', 'pascal')
Energy = QuantityType('Energy', {Mass: 1, Length: 2, Time: -2}, 'J', 'joule')
Power = QuantityType('Power', {Mass: 1, Length: 2, Time: -3}, 'W', 'watt')


# Electrical quantities
Charge = QuantityType('Charge', {Current: 1, Time: 1}, 'C', 'coulomb'),
Voltage = QuantityType('Voltage', {Mass: 1, Length: 2, Time: -3, Current: -1}, 'V', 'volt')
Resistance = QuantityType('Resistance', {Mass: 1, Length: 2, Time: -3, Current: -2}, 'Ω','ohm' )
Conductance = QuantityType('Conductance', {Mass: -1, Length: -2, Time: 3, Current: 2}, 'S','siemens' )
Capacitance = QuantityType('Capacitance', {Mass: -1, Length: -2, Time: 4, Current: 2}, 'F', 'farad')
Inductance = QuantityType('Inductance', {Mass: 1, Length: 2, Time: -2, Current: -2}, 'H', 'henri')
MagneticFlux = QuantityType('Magnetic flux', {Mass: 1, Length: 2, Time: -2, Current: -1}, 'Wb', 'weber')
MagneticFluxDensity = QuantityType('Magnetic flux density', {Mass: 1, Time: -2, Current: -1}, 'T', 'tesla')


# Other
VolumetricFlowRate = QuantityType('VolumetricFlowRate', {Length: 3, Time: -1})
Density = QuantityType('Density', {Mass: 1, Length: -3})
MassFlowRate = QuantityType('MassFlowRate', {Mass: 1, Time: -1})
