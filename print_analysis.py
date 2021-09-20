"""Print analysis rather than writing to file. Useful if only need to check a single property."""


from calculations import update_values, print_amortization_table, print_property_info, print_analysis


update_values(save_to_file=False)  # Initializes everything
print_amortization_table()
print_property_info()
print_analysis()
