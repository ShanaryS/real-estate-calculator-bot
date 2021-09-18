"""Handles updating necessary variables per user input"""


from get_current_interest_rates import interest_rate_30_years, interest_rate_20_years,\
    interest_rate_15_years, interest_rate_10_years, interest_rate_30_years_FHA, interest_rate_30_years_VA
from get_property_info import get_address, get_price, get_property_taxes, get_num_units, get_rent_per_unit


# Values to reset to if no input necessary. A few variables always require input.
DOWN_PAYMENT_PERCENT = 0.20
YEARS = 30
LOAN_TYPE = 'Conventional'
PROPERTY_TAXES = 5000
FIX_UP_COST = 10000
NUM_UNITS = 2
RENT_PER_UNIT = 700
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


# These functions handle not finding certain values that are web scraped
def use_default_property_taxes():
    global found_property_taxes
    found_property_taxes = False
    return PROPERTY_TAXES


def use_default_num_units():
    global found_num_units
    found_num_units = False
    return NUM_UNITS


def use_default_rent_per_unit():
    global found_rent_per_unit
    found_rent_per_unit = False
    return RENT_PER_UNIT


# Values from web scraper.
address = get_address()
price = get_price()
property_taxes = get_property_taxes() if get_property_taxes() > 0 else use_default_property_taxes()
num_units = get_num_units() if get_num_units() > 0 else use_default_num_units()
rent_per_unit = get_rent_per_unit() if get_rent_per_unit() > 0 else use_default_rent_per_unit()

# Handling if some values above were found or is using default
found['Property Taxes'] = (found_property_taxes, property_taxes)
found['Units'] = (found_num_units, num_units)
found['Rent per unit'] = (found_rent_per_unit, rent_per_unit)

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


# TODO UI should handle ValueError and display the message
def set_interest_rate() -> None:
    """Sets interest rate based on loan length"""

    global interest_rate

    if loan_type == 'Conventional':
        if years == 30:
            interest_rate = interest_rate_30_years
        elif years == 20:
            interest_rate = interest_rate_20_years
        elif years == 15:
            interest_rate = interest_rate_15_years
        elif years == 10:
            interest_rate = interest_rate_10_years
        else:
            raise ValueError(f"Invalid combination of loan type '{loan_type}' and years '{years}'.")
    elif loan_type == 'FHA':
        if years == 30:
            interest_rate = interest_rate_30_years_FHA
        else:
            raise ValueError(f"Invalid combination of loan type '{loan_type}' and years '{years}'.")
    elif loan_type == 'VA':
        if years == 30:
            interest_rate = interest_rate_30_years_VA
        else:
            raise ValueError(f"Invalid combination of loan type '{loan_type}' and years '{years}'.")


def update_price(new_price) -> None:
    """Updates price with user input"""
    global price
    price = new_price


def update_down_payment_percent(new_down_payment_percent) -> None:
    """Updates down_payment_percent with user input"""
    global down_payment_percent
    down_payment_percent = new_down_payment_percent


def update_years(new_years) -> None:
    """Updates years with user input"""
    global years
    years = new_years


def update_property_taxes(new_property_taxes) -> None:
    """Updates property_taxes with user input"""
    global property_taxes
    property_taxes = new_property_taxes


def update_closing_percent(new_closing_percent) -> None:
    """Updates closing_percent with user input"""
    global closing_percent
    closing_percent = new_closing_percent


def update_fix_up_cost(new_fix_up_cost) -> None:
    """Updates fix_up_cost with user input"""
    global fix_up_cost
    fix_up_cost = new_fix_up_cost


def update_num_units(new_num_units) -> None:
    """Updates num_units with user input"""
    global num_units
    num_units = new_num_units


def update_rent_per_unit(new_rent_per_unit) -> None:
    """Updates rent_per_unit with user input"""
    global rent_per_unit
    rent_per_unit = new_rent_per_unit


def update_vacancy_percent(new_vacancy_percent) -> None:
    """Updates vacancy_percent with user input"""
    global vacancy_percent
    vacancy_percent = new_vacancy_percent


def update_maintenance_percent(new_maintenance_percent) -> None:
    """Updates maintenance_percent with user input"""
    global maintenance_percent
    maintenance_percent = new_maintenance_percent


def update_management_percent(new_management_percent) -> None:
    """Updates management_percent with user input"""
    global management_percent
    management_percent = new_management_percent


def update_depreciation_short_percent(new_depreciation_short_percent) -> None:
    """Updates depreciation_short_percent with user input"""
    global depreciation_short_percent
    depreciation_short_percent = new_depreciation_short_percent


def update_depreciation_long_percent(new_depreciation_long_percent) -> None:
    """Updates depreciation_long_percent with user input"""
    global depreciation_long_percent
    depreciation_long_percent = new_depreciation_long_percent


def update_tax_bracket(new_tax_bracket) -> None:
    """Updates tax_bracket with user input"""
    global tax_bracket
    tax_bracket = new_tax_bracket


def update_is_first_rental(true_false) -> None:
    """Updates is_first_rental with user input"""
    global is_first_rental
    is_first_rental = true_false
