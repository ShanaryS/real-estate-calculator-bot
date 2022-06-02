import pytest
from src.web.get_property_info import PropertyPage


@pytest.fixture(scope='session')
def property_pages() -> list:
    """List of properties to test with. Need to update urls as zillow listing changes."""

    # Keep these updated as zillow listing changes
    URLS = [
        "https://www.zillow.com/homedetails/101-Mallard-Dr-101-Farmington-CT-06032/2089940072_zpid/",
        "https://www.zillow.com/homedetails/412-Garden-Dr-Batavia-NY-14020/30476735_zpid/",
        "https://www.zillow.com/homedetails/832-Waldo-St-Metairie-LA-70003/73745756_zpid/",
        "https://www.zillow.com/homedetails/11290-Warbonnet-Dr-El-Paso-TX-79936/27426373_zpid/",
        "https://www.zillow.com/homedetails/4999-Kahala-Ave-APT-207-Honolulu-HI-96816/82391182_zpid/"
    ]
    
    return [PropertyPage(url) for url in URLS]


def test_get_address(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        address = page.get_address()
        
        assert isinstance(address, str)  # Is a string
        assert len(address) > 0  # Not empty
        assert int(address.split()[0]) != int(address.split()[-1])  # House # != Zip
        assert len(address.split()[-2]) == 2  # Two letter state code
        assert address.count(",") == 2  # Should be two commas


def test_get_price(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        price = page.get_price()

        assert isinstance(price, int)  # Is an int
        assert price > 10_000  # Is a large positive number


def test_get_year(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        year = page.get_year()

        assert isinstance(year, int)  # Is an int
        assert year > 1600  # -1 is a fail result


def test_get_sqft(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        sqft = page.get_sqft()

        assert isinstance(sqft, int)  # Is an int
        assert sqft > 100  # -1 is a fail case


def test_get_price_per_sqft(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        price_per_sqft = page.get_price_per_sqft()

        assert isinstance(price_per_sqft, int)  # Is an int
        assert price_per_sqft > 10  # -1 is a fail case


def test_get_lot_size(property_pages) -> None:
    page: PropertyPage
    any_found = False
    for page in property_pages:
        lot_size = page.get_lot_size()

        assert isinstance(lot_size, int)  # Is an int

        if lot_size > 100:  # -1 is a fail case, test acre to ft conversion
            any_found = True

    if not any_found:  # If any page passes all tests, it is valid
        pytest.skip("Lot size could not be found...")


def test_get_parking(property_pages) -> None:
    page: PropertyPage
    any_found = False
    for page in property_pages:
        parking = page.get_parking()

        assert isinstance(parking, str)  # Is a string

        if parking != "Unknown":  # If found
            any_found = True

    if not any_found: # If any page passes all tests, it is valid
        pytest.skip("Parking could not be found...")


def test_get_description(property_pages) -> None:
    page: PropertyPage
    any_found = False
    for page in property_pages:
        description = page.get_description()

        assert isinstance(description, str)  # Is a string

        if description != "Unknown":  # If found
            any_found = True

    if not any_found:  # If any page passes all tests, it is valid
        pytest.skip("Parking could not be found...")


def test_get_property_taxes(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        property_taxes = page.get_property_taxes()

        assert isinstance(property_taxes, int)  # Is an int
        assert property_taxes > 10  # -1 is a fail case


def test_get_hoa_fee(property_pages) -> None:
    page: PropertyPage
    any_found = False
    for page in property_pages:
        hoa_fee = page.get_hoa_fee()

        assert isinstance(hoa_fee, int)  # Is an int

        if hoa_fee >= 0:  # If found
            any_found = True

    if not any_found: # If any page passes all tests, it is valid
        pytest.skip("HOA fee could not be found...")


def test_get_num_units(property_pages) -> None:
    page: PropertyPage
    for page in property_pages:
        num_units = page.get_num_units()

        assert isinstance(num_units, tuple)  # Is a tuple
        assert isinstance(num_units[0], int)  # Is an int
        assert isinstance(num_units[1], bool)  # Is a bool
        assert num_units[0] > 0  # Must be positive
        assert num_units[0] < 5  # Cannot be above 5


def test_get_rent_per_unit(property_pages) -> None:
    page: PropertyPage
    any_found = False
    for page in property_pages:
        rent_per_unit = page.get_rent_per_unit()

        assert isinstance(rent_per_unit, tuple)  # Is a tuple
        assert isinstance(rent_per_unit[0], int)  # Is an int
        assert isinstance(rent_per_unit[1], bool)  # Is a bool

        if rent_per_unit[0] > 0:  # If found
            any_found = True

    if not any_found: # If any page passes all tests, it is valid
        pytest.skip("Rent per unit could not be found...")
