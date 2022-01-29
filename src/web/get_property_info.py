"""Web scrapes property info from zillow.com
Uses countyoffice.org/tax-records/ for property taxes if necessary.
"""

from tempfile import TemporaryFile
from bs4 import BeautifulSoup
import requests
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


def _set_url_property_taxes(house_number, street_name, city, state) -> None:
    """Set the county office URL based on the address from zillow"""

    PropertyPage.url_property_taxes = \
        'https://www.countyoffice.org/property-records-search/?q='
    PropertyPage.url_property_taxes += \
        f"{house_number}+{street_name}%2C+{city}%2C+{state}%2C+USA"
    county_office_page = requests.get(PropertyPage.url_property_taxes).text
    PropertyPage.county_office = \
        BeautifulSoup(county_office_page, 'html.parser')


def get_url(property_url=False, taxes_url=False) -> str:
    """Returns URL for either property or property taxes"""

    if property_url:
        return PropertyPage.url_property
    elif taxes_url:
        return PropertyPage.url_property_taxes
    else:
        return PropertyPage.url_property


def get_address() -> str:
    """Get the address of the house from zillow."""

    raw_address = ""
    city_state_zip = ""
    base = PropertyPage.zillow.find(
        'div', class_="ds-home-details-chip").contents[1]

    try:
        raw_address = str(base.span.string).rstrip(',').split()
        city_state_zip = str(base).split('-->')[-1].split('<')[0].split()
    except AttributeError:
        # Sometimes it fails to get the data but it exists.
        # Retrying usually works
        for i in range(NUM_TIMES_TO_RETRY_REQUESTS):
            time.sleep(TIME_BETWEEN_REQUESTS)
            set_page_property_info()
            try:
                raw_address = str(base.span.string).rstrip(',').split()
                city_state_zip = str(base).split('-->')[-1].split(
                    '<')[0].split()
                break
            except AttributeError:
                pass
            if i == NUM_TIMES_TO_RETRY_REQUESTS - 1:
                raw_address = ""
                city_state_zip = ""

    house_number = raw_address[0]
    street_name = ''  # Handled below
    state = city_state_zip.pop(-2)
    zip_code = city_state_zip.pop(-1)
    city = ''  # Handled below

    # street_name can be multiple words, handling it here
    street_name_ = raw_address[1:]
    street_name_length = len(street_name_)
    for index, word in enumerate(street_name_):
        street_name += word
        if index != street_name_length - 1:
            street_name += '+'

    # city can be multiple words, handling it here
    city_ = city_state_zip
    city_[-1] = city_[-1].rstrip(',')
    city_length = len(city_)
    for index, word in enumerate(city_):
        city += word
        if index != city_length - 1:
            city += '+'

    # Saves address into county office url in case zillow has no property taxes.
    _set_url_property_taxes(house_number, street_name, city, state)

    _street_name = ""
    for index, word in enumerate(street_name_):
        _street_name += word
        if index != street_name_length - 1:
            _street_name += ' '

    _city = ""
    for index, word in enumerate(city_):
        _city += word
        if index != city_length - 1:
            _city += ' '

    return f"{house_number} {_street_name}, {_city}, {state} {zip_code}"


def get_price() -> int:
    """Get the price of the listing"""

    price = PropertyPage.zillow.find(class_="ds-summary-row").span.span.span
    price = int(str(price.string).lstrip('$').replace(',', ''))

    return price


def get_year() -> int:
    """Get the year of the listing"""

    house_year = int(PropertyPage.zillow.find(
        class_="ds-home-fact-list-item").next_sibling.contents[-1].string)

    return house_year


def get_sqft() -> int:
    """Get the sqft of the listing"""

    # Assuming values can be acres.
    sqft = float(PropertyPage.zillow.find_all(
        class_="ds-bed-bath-living-area-container")[-1]
                 .contents[-1].span.string.replace(',', ''))

    # House size may be given in acres like lot size for really big houses.
    if sqft > 10:
        sqft = int(sqft)
    else:
        sqft = int(sqft * 43560)
    return sqft


def get_price_per_sqft() -> int:
    """Get the price per sqft of the listing"""

    price_sqft = int(list(PropertyPage.zillow.find(
        class_="ds-home-fact-list-item")
                          .next_siblings)[-1].contents[-1].string.lstrip('$'))

    return price_sqft


def get_lot_size() -> int:
    """Get the lot size of the listing"""

    lot_size = 0
    terms_to_try = ("sc-pbvYO hMYTdE", "sc-qQKeD bSwWwA")

    for i in terms_to_try:
        try:
            lot_size = float(str(PropertyPage.zillow.find_all(
                class_=i)[1].contents[2].span)
                             .split('>')[-2].split('s')[0].replace('Acre', '')
                             .strip().replace(',', ''))
        except (IndexError, ValueError):
            pass

    # Lot size can be sqft or acres so this handles it. Always returns sqft.
    if lot_size > 100:
        lot_size = int(lot_size)
    else:
        lot_size = int(lot_size * 43560)

    return lot_size


def get_parking() -> str:
    """Get parking of the listing"""

    parking = list(PropertyPage.zillow.find(
        class_="ds-home-fact-list-item").next_siblings)[3].contents[-1].string

    return parking


def get_description() -> tuple:
    """Get the description of listing"""

    try:
        description = PropertyPage.zillow.find(
            class_="ds-overview-section").contents[0].contents[0].string
        found_description = True
    except AttributeError:
        description = ""
        found_description = False

    return description, found_description


def get_property_taxes() -> tuple:
    """Get property tax from zillow if it exist. Else use county_office.
    Must call get_address prior.
    """

    property_taxes = 0
    found_property_taxes = True
    check_tax_records = False

    temp = PropertyPage.page.rfind('-->$')

    # Properties with HOA fees or price range in additional details
    # causes finding the wrong values.
    if temp > -1:
        try:
            property_taxes = int(PropertyPage.page[temp+4:temp+11].split('<')[0]
                                 .replace(',', ''))
        except ValueError:
            temp = PropertyPage.page.find('-->$')
            try:
                property_taxes = int(PropertyPage.page[temp + 4:temp + 11]
                                     .split('<')[0].replace(',', ''))
            except ValueError:
                check_tax_records = True

    if check_tax_records:
        try:
            property_taxes = \
                str(PropertyPage.county_office.find_all('tbody')[2]).split(
                    '<td>$')[1].split('<')[0].replace(',', '')
            property_taxes = int(property_taxes)
        except TypeError:
            found_property_taxes = False
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
                    found_property_taxes = False
                    property_taxes = 0

    return property_taxes, found_property_taxes


def get_num_units() -> tuple:
    """Get number of units from zillow. Fall backs to full bathrooms."""

    house_type = PropertyPage.zillow.find(
        class_="ds-home-fact-list-item").contents[-1].string
    found_num_units = True

    if 'single' in house_type.lower():
        num_units = 1
    elif 'duplex' in house_type.lower():
        num_units = 2
    elif 'triplex' in house_type.lower():
        num_units = 3
    elif 'quadruplex' in house_type.lower():
        num_units = 4
    else:
        found_num_units = False
        temp = PropertyPage.page.find('Full bathrooms:')

        if temp > -1:
            num_units = int(PropertyPage.page[temp+24:temp+25])
            num_units = num_units if num_units < 5 else 4
        else:
            num_units = 0

    return num_units, found_num_units


def get_rent_per_unit() -> tuple:
    """Get rent per unit from zillow. If it does not exist, returns 0."""

    temp = PropertyPage.page.find('"pricePerSquareFoot\\":null')-7
    found_rent_per_unit = True

    if temp > -1:
        rent_per_unit = int(
            PropertyPage.page[temp:temp+7].lstrip('"')
            .lstrip(':').rstrip('\\').rstrip(','))
    else:
        found_rent_per_unit = False
        rent_per_unit = 0

    return rent_per_unit, found_rent_per_unit


if __name__ == '__main__':
    set_page_property_info("https://www.zillow.com/homedetails/35-Rackliffe-Dr-New-Britain-CT-06051/57753449_zpid/")
    WATCH = get_price()
    # These don't work
    # price, year, sqft, price_per_sqft, lot size, parking
    # num_units, rent_per_unit?
    pass
