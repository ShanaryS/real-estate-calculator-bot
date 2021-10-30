"""This allows refreshing the listings from all the search URLs without requiring user input. Useful for automation."""

from src.analyses import main as run
from src.property_tracker import add_link


def main() -> None:
    """Main function"""

    add_link(refresh_no_input=True)
    run()


if __name__ == '__main__':
    main()
