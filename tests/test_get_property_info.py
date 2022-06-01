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
        
        assert len(address) > 0  # Not empty
        assert int(address.split()[0]) != int(address.split()[-1])  # House # != Zip
        assert len(address.split()[-2]) == 2  # Two letter state code
        assert address.count(",") == 2  # Should be two commas