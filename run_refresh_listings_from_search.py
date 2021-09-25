"""This allows refreshing the listings from all the search URLs without requiring user input. Useful for automation."""

from run_property_tracker import add_link


if __name__ == '__main__':
    add_link(refresh_no_input=True)
