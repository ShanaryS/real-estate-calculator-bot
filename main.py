from calculations import show_analysis, amortization_table


# Print amortization table
for each_row in zip(*([i] + j for i, j in amortization_table.items())):
    print(*each_row, " ")
