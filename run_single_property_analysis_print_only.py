"""Print analysis rather than writing to file.
Useful if only need to check a single property.
"""

from src.data import update_values, print_property_info, \
    print_analysis, print_sql_amortization_table


def main() -> None:
    """Main function"""

    update_values(save_to_file=False)
    print_sql_amortization_table()
    print_property_info()
    print_analysis()


if __name__ == '__main__':
    main()
