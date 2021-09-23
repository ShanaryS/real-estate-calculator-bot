"""Handles updating necessary variables per user input"""


from web.get_current_interest_rates import set_page_interest_rates, interest_rates
from web.get_property_info import get_address, get_price, get_year, get_description, get_property_taxes,\
    get_num_units, get_rent_per_unit, get_sqft, get_price_per_sqft, get_lot_size, get_parking


# Values to reset to if no input necessary. A few variables always require input.
DOWN_PAYMENT_PERCENT = 0.20
YEARS = 30
LOAN_TYPE = 'Conventional'
PROPERTY_TAXES = 4000
FIX_UP_COST = 10000
NUM_UNITS = 3
RENT_PER_UNIT = 700  # Never used. use_default_rent_per_unit() uses a bit more sophistication in estimation
VACANCY_PERCENT = 0.08
MAINTENANCE_PERCENT = 0.15
MANAGEMENT_PERCENT = 0.10
DEPRECIATION_SHORT_PERCENT = 0.08
DEPRECIATION_LONG_PERCENT = 0.75
TAX_BRACKET = 0.24
IS_FIRST_RENTAL = True

# Variables to keep track if values could not be found and thus used a default value
found_property_taxes = True
found_num_units = True
found_rent_per_unit = True
found = {}

# Values from web scraper
address: str
price: float
year: int
description: str
sqft: int
price_per_sqft: int
lot_size: int
parking: str
property_taxes: int
num_units: int
rent_per_unit: int


def set_info() -> None:
    """Sets the values from html pages"""

    global address, price, year, description, sqft, price_per_sqft
    global lot_size, parking, property_taxes, num_units, rent_per_unit

    tdesc, ttaxes, tnum, trent = get_description(), get_property_taxes(), get_num_units(), get_rent_per_unit()

    address = get_address()
    price = get_price()
    year = get_year()
    description = tdesc[0] if tdesc[1] else tdesc[0]
    sqft = get_sqft()
    price_per_sqft = get_price_per_sqft()
    lot_size = get_lot_size()
    parking = get_parking()
    property_taxes = ttaxes[0] if ttaxes[1] else use_default_property_taxes()
    num_units = tnum[0] if tnum[1] else use_default_num_units(tnum[0])
    rent_per_unit = trent[0] if trent[1] else use_default_rent_per_unit()

    set_found()


def set_found() -> None:
    """Handles if certain values were found or is using default"""

    found['Property Taxes'] = (found_property_taxes, f"{property_taxes:,}")
    found['Units'] = (found_num_units, f"{num_units}")
    found['Rent per unit'] = (found_rent_per_unit, f"{rent_per_unit:,}")


# These functions handle not finding certain values that are web scraped
def use_default_property_taxes() -> int:
    """Returns default value for property_taxes and adjusts relevant variables. Use if property_taxes not found."""
    global found_property_taxes
    found_property_taxes = False
    return PROPERTY_TAXES


def use_default_num_units(_num_units) -> int:
    """Returns default value for num_units and adjusts relevant variables. Use if num_units not found."""
    global found_num_units
    found_num_units = False
    if _num_units > 0:
        return _num_units
    return NUM_UNITS


def use_default_rent_per_unit() -> int:
    """Returns default value for rent_per_unit and adjusts relevant variables. Use if rent_per_unit not found."""
    global found_rent_per_unit
    found_rent_per_unit = False

    if num_units == 1:
        return 1000
    elif num_units == 2:
        return 800
    elif num_units == 3:
        return 650
    elif num_units >= 4:
        return 600


# (INPUT REQUIRED) Default values used for calculator. Variables will be updated when performing real world calculations
# Removed price and num_units to place in web scraper at top of module
interest_rate = 0.04  # Varies depending on years, defined in function below
closing_percent = 0.03

# (INPUT OPTIONAL) Default values used for calculator. Variables will be updated when performing real world calculations
# Removed property_taxers and rent_per_unit to place in web scraper at top of module
down_payment_percent = DOWN_PAYMENT_PERCENT
years = YEARS
loan_type = LOAN_TYPE
fix_up_cost = FIX_UP_COST
vacancy_percent = VACANCY_PERCENT
maintenance_percent = MAINTENANCE_PERCENT
management_percent = MANAGEMENT_PERCENT
depreciation_short_percent = DEPRECIATION_SHORT_PERCENT
depreciation_long_percent = DEPRECIATION_LONG_PERCENT
tax_bracket = TAX_BRACKET
is_first_rental = IS_FIRST_RENTAL


def set_interest_rate() -> None:
    """Sets interest rate based on loan length"""

    set_page_interest_rates()

    global interest_rate

    if loan_type == 'Conventional':
        if years == 30:
            interest_rate = interest_rates['30-year fixed-rate']
        elif years == 20:
            interest_rate = interest_rates['20-year fixed-rate']
        elif years == 15:
            interest_rate = interest_rates['15-year fixed-rate']
        elif years == 10:
            interest_rate = interest_rates['10-year fixed-rate']
        else:
            raise ValueError(f"Invalid combination of loan type '{loan_type}' and years '{years}'.")
    elif loan_type == 'FHA':
        if years == 30:
            interest_rate = interest_rates['30-year fixed-rate FHA']
        else:
            raise ValueError(f"Invalid combination of loan type '{loan_type}' and years '{years}'.")
    elif loan_type == 'VA':
        if years == 30:
            interest_rate = interest_rates['30-year fixed-rate VA']
        else:
            raise ValueError(f"Invalid combination of loan type '{loan_type}' and years '{years}'.")


def get_url_from_input() -> str:
    """Saves user inputted URL"""
    return input()
