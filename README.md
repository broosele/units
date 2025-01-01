# giorgi
A library to work with units and quantities. These can be used for type hints, unit conversion and formatting.


## Quantities

Instances of quantities can be created and printed:
> l0 = Length(10)
> print(l0)
10.000 m

> print(f"{Mass(1, 'g')}, {Mass(3, 'gram')}") 
0.001 kg, 0.003 kg

> print(Time(h=1, min=3, s=5))
3785.000 s

They support basic mathematical operations:
> l1 = Length(20)
> print(4*l0 - l1)
20.000 m

Illegal operations generate errors:
> m0 = Mass(5)
> l0 + m0
TypeError: Can only add quantities of same type together

Resulting quantities can have another Quantity type:
> print(l0*l1)
200.000 m²
> print(type(l0*l1))
Area

Dimensionless quantities are always represented with normal floats and not with a instance of a QuantityType.
> print(type(Time(ms=1)*Frequency(GHz=1)))
<class 'float'>

Supported operations are:

* unary -
* binary - and +: only between quantities of the same type
* *, /: between all quantities, floats or ints
* //, %, divmod: only between quantities of the same type
* **: only between a quantity and an int.
* <, <=, >, >=, ==, !=: between quantities of the same type


## Quantity types

Most common quantity types are predefined.
> Length, Frequency, Force
(QuantityType('Length'), QuantityType('Frequency'), QuantityType('Force'))

You can define your own derived quantities:
> HyperFlowRate = QuantityType('HyperFlowRate', {Length: 4, Time: -1})
QuantityType('HyperFlowRate')

Which automatically gets its own derived main unit:
> HyperFlowRate.main_unit.symbol
'm⁴×s⁻¹'

Quantity types can automatically be derived from others:
> Length**3/Time
QuantityType('VolumetricFlowRate')

This works also if the resulting quantity is not predefined:
> Mass**2/Temperature
QuantityType('Mass2Temperature-1')

Supported operations for quantity types are:
* *, /: between quantity types
* 1/: inversion of a quantity type
* **: only between a quantity type and an int
* ==, !=: between quantity types


## Units
Quantity types can have different units associated with them. They all have a scale, relative to the 'main' unit. Each quantity can be expressed in terms of every unit associated with their quantity type. Many units are predefined.
> l0 = Length(1)
> print(l0.in_unit('mm'))
1000.0
> print(l0.in_unit('"'))
39.370078740157474

Extra units can be created and associated with its quantity:
> Unit(quantity=Length, symbol='Bs', scale=5e-9, name='Beard-second')
Unit('Length', 'Bs', scale=5e-09, bias=0.0)
> print(f"{Length(nm=1):Bs}") 
0.2 Bs

You can also create a whole set of units with different prefices in one go:
> Unit.create_set(quantity=Length, symbol='Bs', scale=5e-9, name='Beard-second')
Unit('Length', 'Bs', scale=5e-09, bias=0.0)
> print(f"{Length(nm=1):μBs}")
200000.0 μBs


## Formatting
Quantities can be formatted using the same formatting mini-language as used for floats, but with the preferred unit at the end:
> print(f"{Volume(hl=1):.>10.6gal}")
...21.9969 gal


## A note about temperatures
Different temperature scales have different starting points. The internal representation of a temperature in
this package is always in Kelvin. This has some potentially unexpected results:
> T0 = Temperature(20, '°C')
> ΔT = Temperature(5, '°C')
> print(f"{T0 + ΔT:°C}")
298.15 °C

This can be easily understood by looking at T0 and ΔT in Kelvin:
> print(f"{T0}, {ΔT}, {T0 + ΔT}")
293.15 K, 278.15 K, 571.3 K

°C and °F are not suited to express differences in temperature as it ambiguous how the values should be interpreted. Instead, use K or °R.
> T0 = Temperature(20, '°C')
> ΔT = Temperature(5, 'K')
> print(f"{T0 + ΔT:°C}")
25.0 °C

Similarly
> T0 = Temperature(20, '°C')
> T1 = Temperature(25, '°C')
> print(f"{T1 - T0:°C}")
-268.15 °C
> print(f"{T1 - T0:K}")
5.0 K


## A note about currencies
Each currency is seen as separate base quantity. The most commonly used currencies are already created,
but you can create your own if needed:
> KRW = BaseQuantityType('South Korean Won', unit_symbol='₩', unit_name='South Korean Won')

To convert between currencies, you need to define a conversion rate:
> won_eur = KRW(1)/EUR(0.00065)
> amount_in_won = KRW(1000_000)
> print(amount_in_euro := amount_in_won/won_eur)
650.000 €


## Things to add
* better system to work with temperatures
* integration of the python standard Time module
* non-integer powers of quantities
* extra formatting options (e.g. ommitting unit)
