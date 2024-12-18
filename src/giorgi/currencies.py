""" giorgi - currencies

This module creates some currencies as base quantities. This means quantities of
different currencies need to be explicitly converted with a conversion factor.

Example:

amount_in_dollar = USD(5)
us_eur = USD(1.05)/EUR(1)
amount_in_euro = amount_in_dollar/us_eur

author: Bram Rooseleer
copyright: Bram Rooseleer
"""


from giorgi.quantities import BaseQuantityType


EUR = BaseQuantityType('Euro', unit_symbol='€', unit_name='Euro')
USD = BaseQuantityType('US dollar', unit_symbol='US$', unit_name='US dollar')
