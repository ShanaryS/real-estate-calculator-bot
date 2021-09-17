"""Handles updating necessary variables per user input"""


# Default values used for calculator. Variables will be updated when performing real world calculations.
price = 200000
down_payment_percent = 0.20
interest_rate = 0.04
years = 30
property_taxes = 3000
closing_percent = 0.03
fix_up_cost = 5000
num_units = 3
rent_per_unit = 700
vacancy_percent = 0.08
maintenance_percent = 0.15
management_percent = 0.10
depreciation_short_percent = 0.08
depreciation_long_percent = 0.75
tax_bracket = 0.24

# Extra information from user
is_first_rental = True  # TODO put this in UI file, update in returns_analysis()


def update_price(new_price) -> None:
    """"""
    global price
    price = new_price


def update_down_payment_percent(new_down_payment_percent) -> None:
    """"""
    global down_payment_percent
    down_payment_percent = new_down_payment_percent


def update_interest_rate(new_interest_rate) -> None:
    """"""
    global interest_rate
    interest_rate = new_interest_rate


def update_years(new_years) -> None:
    """"""
    global years
    years = new_years


def update_property_taxes(new_property_taxes) -> None:
    """"""
    global property_taxes
    property_taxes = new_property_taxes


def update_closing_percent(new_closing_percent) -> None:
    """"""
    global closing_percent
    closing_percent = new_closing_percent


def update_fix_up_cost(new_fix_up_cost) -> None:
    """"""
    global fix_up_cost
    fix_up_cost = new_fix_up_cost


def update_num_units(new_num_units) -> None:
    """"""
    global num_units
    num_units = new_num_units


def update_rent_per_unit(new_rent_per_unit) -> None:
    """"""
    global rent_per_unit
    rent_per_unit = new_rent_per_unit


def update_vacancy_percent(new_vacancy_percent) -> None:
    """"""
    global vacancy_percent
    vacancy_percent = new_vacancy_percent


def update_maintenance_percent(new_maintenance_percent) -> None:
    """"""
    global maintenance_percent
    maintenance_percent = new_maintenance_percent


def update_management_percent(new_management_percent) -> None:
    """"""
    global management_percent
    management_percent = new_management_percent


def update_depreciation_short_percent(new_depreciation_short_percent) -> None:
    """"""
    global depreciation_short_percent
    depreciation_short_percent = new_depreciation_short_percent


def update_depreciation_long_percent(new_depreciation_long_percent) -> None:
    """"""
    global depreciation_long_percent
    depreciation_long_percent = new_depreciation_long_percent


def update_tax_bracket(new_tax_bracket) -> None:
    """"""
    global tax_bracket
    tax_bracket = new_tax_bracket


def update_is_first_rental(true_false) -> None:
    """"""
    global is_first_rental
    is_first_rental = true_false
