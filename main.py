from calculations import get_analysis, get_amortization_table


# Print amortization table
for each_row in zip(*([i] + j for i, j in get_amortization_table().items())):
    print(*each_row, " ")

print()

for key, value in get_analysis().items():
    print(f"{key}: {value}")
