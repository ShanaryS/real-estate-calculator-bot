"""Hub for all the calculations needed"""


import numpy_financial as npf
import json
import user
from get_property_info import get_url


class PrintColors:
    """Used for adding color to print output"""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Basic calculations necessary module wide
down_payment = user.price * user.down_payment_percent
loan = user.price - down_payment
interest_rate_monthly = user.interest_rate / 12
months = user.years * 12
property_taxes_monthly = user.property_taxes / 12
insurance_cost: float

# Defined here for visibility
amortization_table: dict
analysis: dict
property_info: dict
estimations: dict
# Above three defined at bottom of file. Relies on functions below.


def _update_values() -> None:
    """Updates the values when a new property is being evaluated."""

    user.set_interest_rate()

    global down_payment, loan, interest_rate_monthly, months, property_taxes_monthly
    global amortization_table, property_info, analysis, estimations

    down_payment = user.price * user.down_payment_percent
    loan = user.price - down_payment
    interest_rate_monthly = user.interest_rate / 12
    months = user.years * 12
    property_taxes_monthly = user.property_taxes / 12

    amortization_table = mortgage_amortization()
    analysis = returns_analysis()
    property_info = {
        "Address": user.address,
        "Price": user.price,
        "Down Payment": float(f"{user.down_payment_percent * 100:.0f}"),
        "Fix Up Cost": user.fix_up_cost,
        "Loan": float(f"{loan:.0f}"),
        "Interest Rate": float(f"{user.interest_rate * 100:.2f}"),
        "Loan Length": {user.years},
        "Mortgage Payment (Monthly)": float(f"{-amortization_table['Monthly Payment'][0]:.2f}"),
        "Property Taxes (Monthly)": float(f"{property_taxes_monthly:.2f}"),
        "Insurance (Monthly)": float(f"{-insurance_cost / 12:.2f}"),
        "Units": user.num_units,
        "Rent per unit": user.rent_per_unit,
        "Vacancy": float(f"{user.vacancy_percent * 100:.0f}")
    }
    estimations = {item: user.found[item][1] for item, value in user.found.items() if value[0] is False
                   if not all([values[0] for values in user.found.values()])}


def get_amortization_table() -> dict:
    """Get the mortgage amortization table. Second function to interact with."""

    _update_values()

    return amortization_table


def get_info() -> dict:

    _update_values()

    return property_info


def get_analysis() -> dict:
    """Calls required functions needed for analysis. Main function to interact with."""

    _update_values()

    return analysis


def get_estimations() -> dict:
    """"""

    _update_values()

    return estimations


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

    amortization = {'Period': [period], 'Monthly Payment': [monthly_payment],
                    'Principal Payment': [monthly_principal], 'Interest Payment': [monthly_interest],
                    'Loan Balance': [loan_balance]}

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

    global insurance_cost

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
                     'Max Offer (Approximately)': max_offer_string,
                     'Emergency Fund (Recommended)': emergency_fund_string}

    return final_returns


def save_analysis() -> None:
    """Saves analysis of property to analyzedProperties.json"""

    property_analysis = {"Property URL": get_url(property_url=True),
                         "Property Taxes URL": get_url(taxes_url=True),
                         "Property Info": property_info,
                         "Address": user.address,
                         "Price": user.price,
                         "Analysis": analysis,
                         "Estimated": estimations}

    with open('analyzedProperties.json', 'w') as file:
        json.dump(property_analysis, file, indent=4)


def print_amortization_table() -> None:
    """Prints amortization table to terminal"""

    print("Amortization Table:")
    print()
    d = {'Period': [], 'Monthly Payment': [],
         'Principal Payment': [], 'Interest Payment': [],
         'Loan Balance': []}

    for key, value in get_amortization_table().items():
        for num in value:
            if key != 'Period':
                d[key].append(f"{num:.2f}")
            else:
                d[key].append(num)

    for each_row in zip(*([key] + value for key, value in d.items())):
        print(*each_row, " ")
    print("--------------------------------------------")
    print()


def print_property_info() -> None:
    """Prints information gathered about the property"""

    print("Info used for calculations:")
    print()
    print("Property Description -", end=' ')
    if user.description:
        description = user.description
        max_size = 120
        length = len(description)
        slices = int(length / max_size)

        for i in range(slices):
            print(f"{description[i * max_size: (i + 1) * max_size]}", end='')
            if description[(i + 1) * max_size - 1] != ' ' and description[(i + 1) * max_size + 1] != ' ':
                print("-")
            else:
                print("")
        else:
            print(f"{description[slices * max_size:]}")
    else:
        print("None")
    print()
    print(f"Address: {user.address}")
    print(f"Price: ${user.price} - Down Payment: {user.down_payment_percent * 100:.0f}% "
          f"- Fix Up Cost: ${user.fix_up_cost}")
    print(f"Loan: ${loan:.0f} - Interest Rate: {user.interest_rate * 100:.2f}% - Loan Length: {user.years} years")
    print(f"Mortgage Payment (Monthly): ${-amortization_table['Monthly Payment'][0]:.2f} "
          f"- Property Taxes (Monthly): ${property_taxes_monthly:.2f} "
          f"- Insurance (Monthly): ${-insurance_cost / 12:.2f}")
    print(f"Units: {user.num_units} - Rent per unit: ${user.rent_per_unit} "
          f"- Vacancy: {user.vacancy_percent * 100:.0f}%")
    print("--------------------------------------------")
    print()


def print_analysis() -> None:
    """Prints analysis results to terminal"""

    print("Analysis of property:")
    print()

    # Handles printing analysis with color coded results based on how good of a deal it is
    for item in analysis:
        value = analysis[item]
        color = ""
        BAD, OK, GOOD, GREAT = PrintColors.FAIL, PrintColors.WARNING, PrintColors.OKCYAN, PrintColors.OKGREEN

        if item == 'Return On Investment':
            value_check = float(value.rstrip('%'))

            if value_check < 12:
                color = BAD
            if 12 <= value_check < 20:
                color = OK
            if 20 <= value_check < 25:
                color = GOOD
            if value_check >= 25:
                color = GREAT

        elif item == 'Cash on Cash Return':
            value_check = float(value.rstrip('%'))

            if value_check < 8:
                color = BAD
            if 8 <= value_check < 10:
                color = OK
            if 10 <= value_check < 12:
                color = GOOD
            if value_check >= 12:
                color = GREAT

        elif item == 'Caprate':
            value_check = float(value.rstrip('%'))

            if value_check < 5:
                color = BAD
            if 5 <= value_check < 7:
                color = OK
            if 7 <= value_check < 8:
                color = GOOD
            if value_check >= 8:
                color = GREAT

        elif item == 'Cashflow per month':
            value_check = float(value.lstrip('$'))

            if value_check < 150:
                color = BAD
            elif 150 <= value_check < 300:
                color = OK
            elif 300 <= value_check < 500:
                color = GOOD
            elif value_check >= 500:
                color = GREAT

        elif item == 'Max Offer (Approximately)':
            value_check = float(value.lstrip('$'))

            if value_check < user.price * 0.95:
                color = BAD
            elif user.price * 0.95 <= value_check < user.price * 1.05:
                color = OK
            elif user.price * 1.05 <= value_check < user.price * 1.1:
                color = GOOD
            elif value_check >= user.price * 1.1:
                color = GREAT

        print(f"{item}: {color}{value}{PrintColors.ENDC}")

    if not all([values[0] for values in user.found.values()]):
        print()
        print(f"{PrintColors.FAIL}WARNING: THESE ITEMS COULD NOT BE FOUND THUS DEFAULTED TO AN ESTIMATE VALUE. "
              f"THEY MAY BE WRONG.{PrintColors.ENDC}")
        for item, value in user.found.items():
            if value[0] is False:
                print(f"{PrintColors.WARNING}{item}: ??? --> {user.found[item][1]}{PrintColors.ENDC}")
    print("--------------------------------------------")
    print()


_update_values()
