import numpy_financial as npf


# Default values used for calculator. Variables will be updated when performing real world calculations.
price = 200000
down_payment_percent = 0.20
interest_rate = 0.04
years = 30
property_taxes = 3000
fixup_cost = 5000
num_units = 3
rent_per_unit = 700

# Calculated values from above.
down_payment = price * down_payment_percent
loan = price - down_payment
interest_rate_monthly = interest_rate / 12
months = years * 12
property_taxes_monthly = property_taxes / 12

# Calculated after mortgage_amortization(), defined here for visibility
amortization_table: dict


def show_analysis() -> None:
    """Calls required functions needed for analysis. Returns mortgage amortization."""

    global amortization_table

    amortization_table = mortgage_amortization()
    purchase_analysis()
    income_analysis()
    expenses_analysis()
    depreciation_analysis()
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
    global price, down_payment_percent, interest_rate, years, property_taxes, fixup_cost, num_units, rent_per_unit
    global down_payment, loan, interest_rate_monthly, months, property_taxes_monthly

    price = new_price
    down_payment_percent = new_down_payment_percent
    interest_rate = new_interest_rate
    years = new_years
    property_taxes = 3000
    fixup_cost = 5000
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

    Table includes: 'Period', 'Monthly Payment', 'Principal Payment', 'Interest Payment', 'Loan Balance', 'Loan Constant'
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


def purchase_analysis() -> dict:
    """Analysis regarding purchase of the property"""

    pass


def income_analysis() -> dict:
    """Analysis regarding income potential of the property"""

    pass


def expenses_analysis() -> dict:
    """Analysis regarding expenses of the property"""

    pass


def depreciation_analysis() -> dict:
    """Analysis regarding depreciation of the property"""

    pass


def returns_analysis() -> dict:
    """Analysis regarding final returns of the property"""

    pass
