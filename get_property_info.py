"""Web scrapes property info from zillow.com and countyoffice.org/tax-records/ for property taxes if necessary."""


from bs4 import BeautifulSoup
import requests


url_property: str
url_property_taxes: str
zillow: BeautifulSoup
county_office: BeautifulSoup
page: requests.Session()


def set_url_property() -> str:
    """Gets zillow url from user"""

    url = str(input("Enter full url for zillow property:\n"))

    while url[:27] != 'https://www.zillow.com/home':
        url = str(input("Enter full url for zillow property:\n"))
    print()

    return url


def set_page() -> None:
    """Gets html page to parse"""

    global url_property, url_property_taxes, zillow, county_office, page

    # Zillow has bot detection. This handles it.
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    with requests.Session() as s:
        url_property = set_url_property()
        url_property_taxes = 'https://www.countyoffice.org/property-records-search/?q='  # Completed by get_address()
        zillow_page = s.get(url_property, headers=req_headers).text
        page = zillow_page  # Hoping this reduces unnecessary calls to zillow for certain functions

    # Creates beautiful soup object
    zillow = BeautifulSoup(zillow_page, 'html.parser')
    county_office = BeautifulSoup('', 'html.parser')


def _set_url_property_taxes(house_number, street_name, city, state) -> None:
    """Set the county office url based on the address from zillow"""

    global url_property_taxes, county_office

    url_property_taxes = 'https://www.countyoffice.org/property-records-search/?q='  # Resetting variable each func call
    url_property_taxes += f"{house_number}+{street_name}%2C+{city}%2C+{state}%2C+USA"
    county_office_page = requests.get(url_property_taxes).text
    county_office = BeautifulSoup(county_office_page, 'html.parser')


def get_url(property_url=False, taxes_url=False):
    """Returns url for either property or property taxes on countyoffice.org/tax-records/"""

    if property_url:
        return url_property
    elif taxes_url:
        return url_property_taxes
    else:
        return url_property


def get_address() -> str:
    """Get the address of the house from zillow. Use for countyoffice.org/tax-records/"""

    raw_address = str(zillow.find(id="ds-chip-property-address").span).split('>')[1].split(',')[0].split()
    city_state_zip = str(zillow.find(id="ds-chip-property-address")).split('-->')[-1].split('<')[0].split()

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

    # Saves address into county office url in case zillow has no property taxes and need to access it from here.
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
    """Get the price of the house from zillow."""

    price = zillow.find(class_="ds-summary-row").span.span.span
    price = int(str(price).split('>')[1].split('<')[0].lstrip('$').replace(',', ''))

    return price


def get_description() -> tuple:
    """Get the description of listing"""

    try:
        description = zillow.find(class_="Text-c11n-8-48-0__sc-aiai24-0 sc-pQQXS gDpqEw").string
        found_description = True
    except AttributeError:
        description = ""
        found_description = False

    return description, found_description


def get_property_taxes() -> tuple:
    """Get property tax from zillow if it exist. Else use county_office. Must call get_address() prior."""

    temp = page.find('-->$')
    found_property_taxes = True

    if temp > -1:
        property_taxes = int(page[temp+4:temp+9].replace(',', ''))
    else:
        try:
            property_taxes = str(county_office.find_all('tbody')[2]).split('<td>$')[1].split('<')[0].replace(',', '')
            property_taxes = int(property_taxes)
        except TypeError:
            found_property_taxes = False
            property_taxes = 0

    return property_taxes, found_property_taxes


def get_num_units() -> tuple:
    """Get number of units from zillow. Fall backs to full bathrooms as units."""

    house_type = str(zillow.find(class_="ds-home-fact-list-item")).split('>')[-3].split('<')[0]
    found_num_units = True

    if house_type == 'Single Family Residence':
        num_units = 1
    elif house_type == 'Duplex':
        num_units = 2
    elif house_type == 'Triplex':
        num_units = 3
    elif house_type == 'Quadruplex':
        num_units = 4
    else:
        found_num_units = False
        temp = page.find('Full bathrooms:')

        if temp > -1:
            num_units = int(page[temp+24:temp+25])
        else:
            num_units = 0

    return num_units, found_num_units


def get_rent_per_unit() -> tuple:
    """Get rent per unit from zillow. If it does not exist, returns 0."""

    temp = page.find('"pricePerSquareFoot\\":null')-7
    found_rent_per_unit = True

    if temp > -1:
        rent_per_unit = int(page[temp:temp+7].lstrip('"').lstrip(':').rstrip('\\').rstrip(','))
    else:
        found_rent_per_unit = False
        rent_per_unit = 0

    return rent_per_unit, found_rent_per_unit
