"""Web scrapes property info from zillow.com
Uses countyoffice.org/tax-records/ for property taxes if necessary.
"""

from bs4 import BeautifulSoup
import requests
import re
import time
from dataclasses import dataclass

TIME_BETWEEN_REQUESTS = 0
NUM_TIMES_TO_RETRY_REQUESTS = 5


@dataclass
class PropertyPage:
    """Stores info about the property's page"""
    url_property: str
    url_property_taxes: str
    zillow: BeautifulSoup
    county_office: BeautifulSoup
    county_office_saved: bool
    page: requests.models.Response()


def set_page_property_info(url=None) -> None:
    """Gets html page to parse"""

    # Zillow has bot detection. This handles it.
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/'
                  'xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    with requests.Session() as s:
        PropertyPage.url_property = _set_url_property(url)
        zillow_page = s.get(PropertyPage.url_property, headers=req_headers).text
        PropertyPage.page = zillow_page

    # Creates beautiful soup object
    PropertyPage.zillow = BeautifulSoup(zillow_page, 'html.parser')
    PropertyPage.county_office = BeautifulSoup('', 'html.parser')
    PropertyPage.county_office_saved = False


def _set_url_property(url=None) -> str:
    """Gets zillow URL from user or file when running analysis"""

    if url:
        _url = url
    else:
        _url = input("Enter full URL for zillow property: ")

        while _url[:27] != 'https://www.zillow.com/home' or len(_url) < 35:
            _url = str(input("Enter full URL for zillow property: "))
        print("\n---   Gathering data for analysis...   ---\n")

    return _url


def _set_county_office_url(house_number, street_name, city, state) -> None:
    """Set the county office URL based on the address from zillow"""

    PropertyPage.url_property_taxes = 'https://www.countyoffice.org/property-records-search/?q='
    PropertyPage.url_property_taxes += f"{house_number}+{street_name}%2C+{city}%2C+{state}%2C+USA"


def _save_county_office_page() -> None:
    """Gets the alternate property taxes used as a fallback"""
    
    if not PropertyPage.county_office_saved:
        county_office_page = requests.get(PropertyPage.url_property_taxes).text
        PropertyPage.county_office = BeautifulSoup(county_office_page, 'html.parser')


def get_url(property_url=False, taxes_url=False) -> str:
    """Returns URL for either property or property taxes"""

    if property_url:
        return PropertyPage.url_property
    elif taxes_url:
        return PropertyPage.url_property_taxes
    else:
        return PropertyPage.url_property


def get_address() -> str:
    """Get the address of the house from zillow. Raises error if not found."""

    # Use the title of the browser tab for address
    full_address = PropertyPage.zillow.find("title").string.split("|")[0].strip()

    # Saves address into county office url in case zillow has no property taxes.
    house_number = full_address.split()[0]
    street_name = " ".join(full_address.split(",")[0].split()[1:])
    city = full_address.split(",")[1].strip()
    state = full_address.split(",")[2].split()[0]
    zip_code = full_address.split(",")[2].split()[1]
    _set_county_office_url(house_number, street_name, city, state)

    return f"{house_number} {street_name}, {city}, {state} {zip_code}"


def get_price() -> int:
    """Get the price of the listing. Raises error if not found."""

    # House price is almost guaranteed to be first
    price_str = PropertyPage.zillow.find("span", string=re.compile("\$")).string
    price = int(price_str.lstrip('$').replace(',', ''))
    
    return price


def get_year() -> int:
    """Get the year of the listing. Returns -1 if not found."""

    # House year typically in form of "Built in XXXX"
    try:
        built_in_year_str = PropertyPage.zillow.find("span", string=re.compile("Built")).string
        house_year = int(built_in_year_str.split()[-1])
    except Exception:
        house_year = -1

    return house_year


def get_sqft() -> int:
    """Get the sqft of the listing. Returns -1 if not found."""

    # Use price/sqft value and calculate from price
    try:
        price_per_sqft_str = PropertyPage.zillow.find("span", string=re.compile("price/sqft")).string
        sqft = int(get_price()/int(price_per_sqft_str.lstrip("$").split()[0]))
    except Exception:
        sqft = -1
   
    return sqft


def get_price_per_sqft() -> int:
    """Get the price per sqft of the listing. Returns -1 if not found."""

    # Usually in the form "$XXX price/sqft"
    try:
        price_per_sqft_str = PropertyPage.zillow.find("span", string=re.compile("price/sqft")).string
        price_per_sqft = int(price_per_sqft_str.lstrip("$").split()[0])
    except Exception:
        price_per_sqft = -1

    return price_per_sqft


def get_lot_size() -> int:
    """Get the lot size of the listing in sqft. Returns -1 if not found"""

    lot_size = -1  # Some may not list a lot size

    # Usually in the form "Lot size: XXX Acres" or "Lot size: X,XXX sqft"
    # The span that contains a lot size only has text not a string
    spans = PropertyPage.zillow.find_all("span")
    temp = ""
    for i in spans:
        if "lot size:" in i.text.lower():
            temp = i.text
            break
    if temp:
        temp = temp.split()
        unit = temp[-1]
        num_string = temp[-2]
        lot_size = float(num_string.replace(",", ""))

        if "acres" in unit.lower():
            lot_size = int(lot_size * 43560)  # Convert acres to sqft

    return lot_size


def get_parking() -> str:
    """Get parking of the listing. Returns 'Unknown' if not found."""
    parking = "Unknown"

    # Only care about number of spaces
    parking_strs = PropertyPage.zillow.find_all("span")
    for i in parking_strs:
        if "total spaces:" in i.text.lower():
            parking = i.text

    return parking


def get_description() -> str:
    """Get the description of listing. Returns 'Unknown' if not found."""
    description = "Unknown"

    # Find description if there is a "Read More" button. Likely to fail but not important
    temp = PropertyPage.zillow.find("button", string="Read more").previous_element
    if temp:
        description = temp
    
    return description


def get_property_taxes() -> int:
    """Get property tax from zillow if it exist. Else use county_office. Returns -1 if not found.
    Must call get_address prior.
    """

    # Try to find taxes on zillow page first, if not exist fall back to county office
    property_taxes = -1
    check_tax_records = True

    # Find on zillow
    spans = PropertyPage.zillow.find_all("span")
    temp = ""
    for i in spans:
        if "annual tax amount:" in i.text.lower():
            temp = i.text
            break
    if temp:
        check_tax_records = False
        property_taxes = int(temp.split()[-1].lstrip("$").replace(",", ""))

    # Find on county office
    if check_tax_records:
        _save_county_office_page()
        try:
            property_taxes = \
                str(PropertyPage.county_office.find_all('tbody')[2]).split(
                    '<td>$')[1].split('<')[0].replace(',', '')
            property_taxes = int(property_taxes)
        except TypeError:
            property_taxes = 0
        except IndexError:
            # Sometimes it fails to get the data but it exists.
            # Retrying usually works
            for i in range(NUM_TIMES_TO_RETRY_REQUESTS):
                time.sleep(TIME_BETWEEN_REQUESTS)
                get_address()
                try:
                    property_taxes = str(
                        PropertyPage.county_office.find_all('tbody')[2])\
                        .split('<td>$')[1].split('<')[0].replace(',', '')
                    property_taxes = int(property_taxes)
                    break
                except (TypeError, IndexError):
                    pass
                if i == NUM_TIMES_TO_RETRY_REQUESTS - 1:
                    property_taxes = -1

    return property_taxes


def get_hoa_fee() -> int:
    """Get the HOA fees. Returns -1 if not found but 0 if there is none."""
    hoa_fee = -1

    spans = PropertyPage.zillow.find_all("span")
    temp = ""
    for i in spans:
        if "has hoa:" in i.text.lower():
            temp = i.text
            break
    if temp:
        yes_no = temp.split(":")[-1].strip()
        if "no" in yes_no.lower():
            hoa_fee = 0
        else:
            # Find the HOA amount
            spans = PropertyPage.zillow.find_all("span")
            temp = ""
            for i in spans:
                if "hoa fee:" in i.text.lower():
                    temp = i.text
                    break
            if temp:
                hoa_fee = int(temp.split("$")[-1].split()[0])

    return hoa_fee


def get_num_units() -> tuple:
    """Get number of units from zillow. Fall backs to hueristics if not found.
    Must call get address prior.
    """

    # Look for explict mention of num units otherwise fall back to hueristics
    # Assuming max num units is 4 as above is considered an apartment
    num_units = None
    house_type = ""
    found_num_units = True
    check_tax_records = False
    
    spans = PropertyPage.zillow.find_all("span")
    temp = ""
    for i in spans:
        if "property subtype:" in i.text.lower():
            temp = i.text
            break
    if temp:
        house_type = temp.split(":")[-1].strip()

    def parse_house_type():
        nonlocal num_units, house_type, found_num_units, check_tax_records
        if 'single' in house_type.lower() or 'condo' in house_type.lower():
            num_units = 1
        elif 'duplex' in house_type.lower():
            num_units = 2
        elif 'triplex' in house_type.lower():
            num_units = 3
        elif 'quad' in house_type.lower():
            num_units = 4
        else:
            found_num_units = False
            check_tax_records = True
            num_units = 1
            if 'multi family' in house_type.lower() or 'multifamily' in house_type.lower():
                num_units = 4  # Assume 4 units to either be accurate or get a false positive

    parse_house_type()

    if check_tax_records:
        found_num_units = True
        _save_county_office_page()
        spans = PropertyPage.county_office.find_all("span", class_="pd-p")
        for span in spans:
            if "residential" in span.previous_sibling.lower():
                house_type = span.string
                break
        parse_house_type()

    return num_units, found_num_units


def get_rent_per_unit() -> tuple:
    """Get rent per unit from zillow. If it does not exist, returns -1."""

    # Scan the raw text of the document as rent listings are loaded dynamically
    rent_per_unit = -1
    found_rent_per_unit = False
    temp = PropertyPage.page.find('"pricePerSquareFoot\\":null')-7

    if temp > -1:
        found_rent_per_unit = True
        rent_per_unit = int(
            PropertyPage.page[temp:temp+7].lstrip('"')
            .lstrip(':').rstrip('\\').rstrip(','))

    return rent_per_unit, found_rent_per_unit


if __name__ == '__main__':
    set_page_property_info("https://www.zillow.com/homedetails/101-Mallard-Dr-101-Farmington-CT-06032/2089940072_zpid/")
    print(f"---Address: {get_address()}")
    print(f"---Price: {get_price()}")
    print(f"---Year: {get_year()}")
    print(f"---Sqft: {get_sqft()}")
    print(f"---Price/Sqft: {get_price_per_sqft()}")
    print(f"---Lot Size: {get_lot_size()}")
    print(f"---Parking: {get_parking()}")
    print(f"---Description: {get_description()}")
    print(f"---Property Taxes: {get_property_taxes()}")
    print(f"---HOA: {get_hoa_fee()}")
    print(f"---Num Units: {get_num_units()}")
    print(f"---Rent per unit: {get_rent_per_unit()}")
