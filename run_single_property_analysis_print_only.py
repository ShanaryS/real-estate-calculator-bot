"""Print analysis rather than writing to file.
Useful if only need to check a single property.
"""

from src.data.calculations import update_values, print_property_info, \
    print_analysis, print_sql_amortization_table
from src.data.colors_for_print import BAD, OK, GOOD, GREAT, END


def main() -> None:
    """Main function"""

    if not update_values(save_to_file=False):
        print(f" {BAD}!!! ERROR ANALYZING THIS PROPERTY. "
              f"CHECK \\output\\errors.log FOR DETAILS. !!!{END}"
              )
        input('Press Enter to close program...')
        return
    print_sql_amortization_table()
    print_property_info()
    print_analysis()
    input('Press Enter to close program...')


if __name__ == '__main__':
    main()
