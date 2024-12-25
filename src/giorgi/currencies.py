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
GBP = BaseQuantityType('British Pound', unit_symbol='£', unit_name='British Pound')
JPY = BaseQuantityType('Japanese Yen', unit_symbol='¥', unit_name='Japanese Yen')
CNY = BaseQuantityType('Chinese Yuan', unit_symbol='CN¥', unit_name='Chinese Yuan')
CHF = BaseQuantityType('Swiss Franc', unit_symbol='fr.', unit_name='Swiss Franc')
SEK = BaseQuantityType('Swedish Krona', unit_symbol='kr', unit_name='Swedish Krona')
USD = BaseQuantityType('US Dollar', unit_symbol='$', unit_name='US Dollar')
CAD = BaseQuantityType('Canadian Dollar', unit_symbol='CA$', unit_name='Canadian Dollar')
AUD = BaseQuantityType('Australian Dollar', unit_symbol='AU$', unit_name='Australian Dollar')
NZD = BaseQuantityType('New Zealand Dollar', unit_symbol='NZ$', unit_name='New Zealand Dollar')
SGD = BaseQuantityType('Singapore Dollar', unit_symbol='S$', unit_name='Singapore Dollar')
HKD = BaseQuantityType('Hong Kong Dollar', unit_symbol='HK$', unit_name='Hong Kong Dollar')
