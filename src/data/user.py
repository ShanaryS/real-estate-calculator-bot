"""Handles updating necessary variables per user input"""

from dataclasses import dataclass

from src.web.get_current_interest_rates \
    import set_page_interest_rates, InterestRates
from src.web.get_property_info \
    import get_address, get_price, get_year, get_description, \
    get_property_taxes, get_num_units, get_rent_per_unit, get_sqft, \
    get_price_per_sqft, get_lot_size, get_parking
from values import *


@dataclass
class UserValues:
    """Values that the user inputs. Default found in values.py."""
    down_payment_percent = DOWN_PAYMENT_PERCENT
    years = YEARS
    loan_type = LOAN_TYPE
    fix_up_cost = FIX_UP_COST
    closing_percent = CLOSING_PERCENT
    vacancy_percent = VACANCY_PERCENT
    maintenance_percent = MAINTENANCE_PERCENT
    management_percent = MANAGEMENT_PERCENT
    depreciation_short_percent = DEPRECIATION_SHORT_PERCENT
    depreciation_long_percent = DEPRECIATION_LONG_PERCENT
    tax_bracket = TAX_BRACKET
    is_first_rental = IS_FIRST_RENTAL


@dataclass
class WebScraper:
    """Values retrieved from web scraper"""
    address: str
    price: float
    interest_rate: float
    year: int
    description: str
    sqft: int
    price_per_sqft: int
    lot_size: int
    parking: str
    property_taxes: int
    num_units: int
    rent_per_unit: int
    found_property_taxes = True
    found_num_units = True
    found_rent_per_unit = True
    found = {}


def set_info() -> None:
    """Sets the values from html pages"""

    tdesc, ttaxes, tnum, trent = get_description(), get_property_taxes(), \
                                 get_num_units(), get_rent_per_unit()

    WebScraper.address = get_address()
    WebScraper.price = get_price()
    WebScraper.year = get_year()
    WebScraper.description = tdesc[0] if tdesc[1] else tdesc[0]
    WebScraper.sqft = get_sqft()
    WebScraper.price_per_sqft = get_price_per_sqft()
    WebScraper.lot_size = get_lot_size()
    WebScraper.parking = get_parking()
    WebScraper.property_taxes = ttaxes[0] if ttaxes[1] \
        else use_default_property_taxes()
    WebScraper.num_units = tnum[0] if tnum[1] \
        else use_default_num_units(tnum[0])
    WebScraper.rent_per_unit = trent[0] if trent[1] \
        else use_default_rent_per_unit()

    set_found()


def set_found() -> None:
    """Handles if certain values were found or is using default"""

    WebScraper.found['Property Taxes'] = (WebScraper.found_property_taxes,
                                          f"{WebScraper.property_taxes:,}")
    WebScraper.found['Units'] = (WebScraper.found_num_units,
                                 f"{WebScraper.num_units}")
    WebScraper.found['Rent Per Unit ($)'] = (WebScraper.found_rent_per_unit,
                                             f"{WebScraper.rent_per_unit:,}")


# These functions handle not finding certain values that are web scraped
def use_default_property_taxes() -> int:
    """Returns default value for property_taxes and adjusts relevant variables.
    Use if property_taxes not found.
    """
    WebScraper.found_property_taxes = False
    return PROPERTY_TAXES


def use_default_num_units(_num_units) -> int:
    """Returns default value for num_units and adjusts relevant variables.
    Use if num_units not found.
    """
    WebScraper.found_num_units = False
    if _num_units > 0:
        return _num_units
    return NUM_UNITS


def use_default_rent_per_unit() -> int:
    """Returns default value for rent_per_unit and adjusts relevant variables.
    Use if rent_per_unit not found.
    """
    WebScraper.found_rent_per_unit = False

    if WebScraper.num_units == 1:
        return RENT_PER_UNIT_SINGLE
    elif WebScraper.num_units == 2:
        return RENT_PER_UNIT_DUPLEX
    elif WebScraper.num_units == 3:
        return RENT_PER_UNIT_TRIPLEX
    elif WebScraper.num_units >= 4:
        return RENT_PER_UNIT_DUPLEX


def set_interest_rate() -> None:
    """Sets interest rate based on loan length"""

    set_page_interest_rates()

    if UserValues.loan_type == 'Conventional':
        if UserValues.years == 30:
            WebScraper.interest_rate = \
                InterestRates.interest_rates['30-year fixed-rate']
        elif UserValues.years == 20:
            WebScraper.interest_rate = \
                InterestRates.interest_rates['20-year fixed-rate']
        elif UserValues.years == 15:
            WebScraper.interest_rate = \
                InterestRates.interest_rates['15-year fixed-rate']
        elif UserValues.years == 10:
            WebScraper.interest_rate = \
                InterestRates.interest_rates['10-year fixed-rate']
        else:
            raise ValueError(f"Invalid combination of loan type "
                             f"'{UserValues.loan_type}' and years "
                             f"'{UserValues.years}'."
                             )
    elif UserValues.loan_type == 'FHA':
        if UserValues.years == 30:
            WebScraper.interest_rate = \
                InterestRates.interest_rates['30-year fixed-rate FHA']
        else:
            raise ValueError(f"Invalid combination of loan type "
                             f"'{UserValues.loan_type}' and years "
                             f"'{UserValues.years}'."
                             )
    elif UserValues.loan_type == 'VA':
        if UserValues.years == 30:
            WebScraper.interest_rate = \
                InterestRates.interest_rates['30-year fixed-rate VA']
        else:
            raise ValueError(f"Invalid combination of loan type "
                             f"'{UserValues.loan_type}' and years "
                             f"'{UserValues.years}'."
                             )


def get_url_from_input() -> str:
    """Saves user inputted URL"""
    return input()
