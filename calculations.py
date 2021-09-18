"""Hub for all the calculations needed"""


import numpy_financial as npf
import user


# Basic calculations necessary module wide
down_payment = user.price * user.down_payment_percent
loan = user.price - down_payment
interest_rate_monthly = user.interest_rate / 12
months = user.years * 12
property_taxes_monthly = user.property_taxes / 12

# Defined here for visibility
amortization_table: dict


def get_analysis() -> dict:
    """Calls required functions needed for analysis. Main function to interact with."""

    _update_values()

    return returns_analysis()


def get_amortization_table() -> dict:
    """Get the mortgage amortization table. Second function to interact with."""

    _update_values()

    return amortization_table


# TODO Different interest rates based on years
def _update_values() -> None:

    """Updates the values when a new property is being evaluated."""

    global down_payment, loan, interest_rate_monthly, months, property_taxes_monthly, amortization_table

    down_payment = user.price * user.down_payment_percent
    loan = user.price - down_payment
    interest_rate_monthly = user.interest_rate / 12
    months = user.years * 12
    property_taxes_monthly = user.property_taxes / 12

    amortization_table = mortgage_amortization()


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


def purchase_analysis() -> float:
    """Amount required to purchase the property"""

    closing_cost = loan * user.closing_percent

    return down_payment + user.fix_up_cost + closing_cost


def income_analysis() -> float:
    """Effective gross income of the property"""

    rent = user.rent_per_unit * user.num_units
    gross_potential_income = rent * 12
    vacancy_cost = -(gross_potential_income * user.vacancy_percent)
    effective_gross_income = gross_potential_income + vacancy_cost

    return effective_gross_income


def expenses_analysis() -> float:
    """Cost of owning of the property"""

    effective_gross_income = income_analysis()

    maintenance_cost = -(effective_gross_income * user.maintenance_percent)
    management_cost = -(effective_gross_income * user.management_percent)
    property_taxes_cost = -user.property_taxes
    insurance_cost = -(user.price * 0.00425)
    total_cost = maintenance_cost + management_cost + property_taxes_cost + insurance_cost

    return total_cost


def profit_analysis() -> tuple:
    """Cashflow, net income, and yearly cost of property"""

    effective_gross_income = income_analysis()
    total_cost = expenses_analysis()
    net_operating_income = effective_gross_income + total_cost

    debt_service = amortization_table['Monthly Payment'][0] * 12
    cashflow = net_operating_income + debt_service

    yearly_cost = total_cost + debt_service

    return cashflow, net_operating_income, yearly_cost


def depreciation_analysis() -> float:
    """Taxes saved by depreciation of the property"""

    depreciation_short_total = (user.price + user.fix_up_cost) * user.depreciation_short_percent
    depreciation_short_yearly = depreciation_short_total / 5

    depreciation_long_total = (user.price + user.fix_up_cost) * user.depreciation_long_percent
    depreciation_long_yearly = depreciation_long_total / 27.5

    tax_exposure_decrease = (depreciation_short_yearly + depreciation_long_yearly) * user.tax_bracket

    return tax_exposure_decrease


def returns_analysis() -> dict:
    """Yearly returns of the property along with extra details"""

    capital_required = purchase_analysis()
    cashflow, net_operating_income, yearly_cost = profit_analysis()
    effective_gross_income = income_analysis()
    tax_exposure_decrease = depreciation_analysis()
    principal_paydown = -sum(amortization_table['Principal Payment'][0:12])
    total_return = cashflow + tax_exposure_decrease + principal_paydown

    return_on_investment_percent = round(total_return / capital_required * 100, 2)
    c_on_c_return_percent = round(cashflow / capital_required * 100, 2)
    caprate_percent = round(net_operating_income / user.price * 100, 2)
    cashflow_per_month = cashflow / 12
    max_offer = ((effective_gross_income * 0.75 + -user.property_taxes - 600) * (0.37/0.12))\
        / (user.closing_percent + user.down_payment_percent) - user.fix_up_cost
    emergency_fund = -yearly_cost / 2 if user.is_first_rental else -yearly_cost / 4

    return_on_investment_string = f"{return_on_investment_percent}%"
    c_on_c_return_string = f"{c_on_c_return_percent}%"
    caprate_string = f"{caprate_percent}%"
    cashflow_per_month_string = f"${cashflow_per_month:.2f}"
    max_offer_string = f"${max_offer:.2f}"
    emergency_fund_string = f"${emergency_fund:.2f}"

    final_returns = {'Return On Investment': return_on_investment_string,
                     'Cash on Cash Return': c_on_c_return_string,
                     'Caprate': caprate_string,
                     'Cashflow per month': cashflow_per_month_string,
                     'Max Offer': max_offer_string,
                     'Emergency Fund': emergency_fund_string}

    return final_returns
