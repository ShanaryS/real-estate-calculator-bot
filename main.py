import calculations as calc


price = 200000
down_payment = 0.20 * price
interest_rate = 0.04
years = 30

amortization_table = calc.mortgage_amortization(price, down_payment, interest_rate, years)

print(amortization_table)
