import numpy_financial as npf


# Default values used for calculator. Variables will be updated when performing real world calculations.
price = 200000
down_payment_percent = 0.20
interest_rate = 0.04
years = 30
property_taxes = 3000
closing_percentage = 0.03
fix_up_cost = 5000
num_units = 3
rent_per_unit = 700
vacancy_percent = 0.08
maintenance_percent = 0.15
management_percent = 0.10
depreciation_short_percent = 0.08
depreciation_long_percent = 0.75
tax_bracket = 0.24

# Calculated values from above.
down_payment = price * down_payment_percent
loan = price - down_payment
interest_rate_monthly = interest_rate / 12
months = years * 12
property_taxes_monthly = property_taxes / 12

# Calculated after mortgage_amortization(), defined here for visibility
amortization_table: dict

# Extra information from user
is_first_rental = True


def show_analysis() -> None:
    """Calls required functions needed for analysis. Returns mortgage amortization."""

    global amortization_table

    amortization_table = mortgage_amortization()
    returns_analysis()

    # TODO add show GUI here?


# TODO Different interest rates based on years
def update_values(new_price=price,
                  new_down_payment_percent=down_payment_percent,
                  new_interest_rate=interest_rate,
                  new_years=years) \
                  -> None:

    """Updates the values when a new property is being evaluated."""

    # Updating variables from outside the function
    global price, down_payment_percent, interest_rate, years, property_taxes, fix_up_cost, num_units, rent_per_unit
    global down_payment, loan, interest_rate_monthly, months, property_taxes_monthly

    # TODO negative values for ones that need to be negative
    price = new_price
    down_payment_percent = new_down_payment_percent
    interest_rate = new_interest_rate
    years = new_years
    property_taxes = 3000
    fix_up_cost = 5000
    num_units = 3
    rent_per_unit = 700

    down_payment = price * down_payment_percent
    loan = price - down_payment
    interest_rate_monthly = interest_rate / 12
    months = years * 12
    property_taxes_monthly = property_taxes / 12

    # Updating analysis
    show_analysis()


def mortgage_amortization() -> dict:
    """Returns amortization table for given args. If no args, defaults to constants in calculations.py

    Table includes: 'Period', 'Monthly Payment', 'Principal Payment', 'Interest Payment', 'Loan Balance',
    and 'Loan Constant'
    """

    period = 1
    monthly_payment = npf.pmt(interest_rate_monthly, months, loan)
    monthly_principal = npf.ppmt(interest_rate_monthly, period, months, loan)
    monthly_interest = npf.ipmt(interest_rate_monthly, period, months, loan)
    loan_balance = npf.fv(interest_rate_monthly, period, monthly_payment, loan)
    loan_constant = monthly_payment / loan

    amortization = {'Period': [period], 'Monthly Payment': [monthly_payment],
                    'Principal Payment': [monthly_principal], 'Interest Payment': [monthly_interest],
                    'Loan Balance': [loan_balance], 'Loan Constant': [loan_constant]}

    for i in range(2, months+1):
        period = i
        monthly_principal = npf.ppmt(interest_rate_monthly, period, months, loan)
        monthly_interest = npf.ipmt(interest_rate_monthly, period, months, loan)
        loan_balance = npf.fv(interest_rate_monthly, period, monthly_payment, loan)

        amortization['Period'].append(period)
        amortization['Monthly Payment'].append(monthly_payment)
        amortization['Principal Payment'].append(monthly_principal)
        amortization['Interest Payment'].append(monthly_interest)
        amortization['Loan Balance'].append(loan_balance)
        amortization['Loan Constant'].append(loan_constant)

    return amortization


# Storing amortization table here for easy updating
amortization_table = mortgage_amortization()


def purchase_analysis() -> float:
    """Amount required to purchase the property"""

    closing_cost = loan * closing_percentage

    return down_payment + fix_up_cost + closing_cost


def income_analysis() -> float:
    """Effective gross income of the property"""

    rent = rent_per_unit * num_units
    gross_potential_income = rent * 12
    vacancy_cost = -(gross_potential_income * vacancy_percent)
    effective_gross_income = gross_potential_income - vacancy_cost

    return effective_gross_income


def expenses_analysis() -> float:
    """Cost of owning of the property"""

    effective_gross_income = income_analysis()

    maintenance_cost = -(effective_gross_income * maintenance_percent)
    management_cost = -(effective_gross_income * management_percent)
    property_taxes_cost = -property_taxes
    insurance_cost = -(price * 0.00425)
    total_cost = maintenance_cost + management_cost + property_taxes_cost + insurance_cost

    return total_cost


def profit_analysis() -> tuple:
    """Cashflow, net income, and yearly cost of property"""

    effective_gross_income = income_analysis()
    total_cost = expenses_analysis()
    net_operating_income = effective_gross_income - total_cost

    debt_service = amortization_table['Monthly Payment'][0] * 12
    cashflow = net_operating_income - debt_service

    yearly_cost = total_cost + debt_service

    return cashflow, net_operating_income, yearly_cost


def depreciation_analysis() -> float:
    """Analysis regarding depreciation of the property"""

    depreciation_short_total = (price + fix_up_cost) * depreciation_short_percent
    depreciation_short_yearly = depreciation_short_total / 5

    depreciation_long_total = (price + fix_up_cost) * depreciation_long_percent
    depreciation_long_yearly = depreciation_long_total / 27.5

    depreciation_total = (depreciation_short_yearly + depreciation_long_yearly) * tax_bracket

    return depreciation_total


def returns_analysis() -> dict:
    """Yearly returns of the property"""

    capital_required = purchase_analysis()
    cashflow, net_operating_income, yearly_cost = profit_analysis()
    effective_gross_income = income_analysis()

    principal_paydown = -sum(amortization_table['Principal Payment'][0:12])
    tax_exposure_decrease = depreciation_analysis()
    total_return = cashflow + principal_paydown + tax_exposure_decrease

    return_on_investment = total_return / capital_required
    c_on_c_return = cashflow / capital_required
    caprate = price / net_operating_income
    cashflow_per_month = cashflow / 12
    max_offer = ((effective_gross_income * 0.75 + -property_taxes - 600) * (0.37/0.12))\
        / (closing_percentage + down_payment_percent) - fix_up_cost
    emergency_fund = yearly_cost / 2 if is_first_rental else yearly_cost / 4

    final_returns = {'Return On Investment': return_on_investment,
                     'Cash on Cash Return': c_on_c_return,
                     'Caprate': caprate,
                     'Cashflow per month': cashflow_per_month,
                     'Max Offer': max_offer,
                     'Emergency Fund': emergency_fund}

    return final_returns
