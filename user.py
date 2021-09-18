"""Handles updating necessary variables per user input"""


from get_current_interest_rates import interest_rate_30_years, interest_rate_20_years,\
    interest_rate_15_years, interest_rate_10_years, interest_rate_30_years_FHA, interest_rate_30_years_VA


# Default values used for calculator. Variables will be updated when performing real world calculations.
price = 200000
down_payment_percent = 0.20
years = 30
interest_rate = 0.04  # Varies depending on years, defined in function below
loan_type = 'Conventional'
property_taxes = 5300
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
is_first_rental = True


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
