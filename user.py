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

# Extra information from user
is_first_rental = True  # TODO put this in UI file, update in returns_analysis()
