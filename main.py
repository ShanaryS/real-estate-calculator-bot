import calculations as calc


price = 200000
down_payment_percent = 0.20
interest_rate = 0.04
years = 30

amortization_table = calc.mortgage_amortization(price, down_payment_percent, interest_rate, years)

print(amortization_table)
