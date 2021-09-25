"""Print analysis rather than writing to file. Useful if only need to check a single property."""

from data.calculations import update_values, print_amortization_table, print_property_info, print_analysis


if __name__ == '__main__':
    update_values(save_to_file=False)
    print_amortization_table()
    print_property_info()
    print_analysis()
