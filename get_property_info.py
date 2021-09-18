"""Web scrapes property info from zillow.com and countyoffice.org/tax-records/ for property taxes if necessary."""


from bs4 import BeautifulSoup
import requests


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
    url_property = 'https://www.zillow.com/homedetails/21-Harvard-St-Waterbury-CT-06704/58007082_zpid/'
    page = s.get(url_property, headers=req_headers).text


# TODO Set url based on user link, later do it automatically whenever new listings get posted or price updates
# Creates beautiful soup object
url_property = 'https://www.zillow.com/homedetails/21-Harvard-St-Waterbury-CT-06704/58007082_zpid/'
doc = BeautifulSoup(page, 'html.parser')

# Parses html for address
raw_address = str(doc.find(id="ds-chip-property-address").span).split('>')[1].split(',')[0].split()
city_state_zip = str(doc.find(id="ds-chip-property-address")).split('-->')[-1].split('<')[0].split()

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
url_property_taxes = 'https://www.countyoffice.org/property-records-search/?q='
url_property_taxes += f"{house_number}+{street_name}%2C+{city}%2C+{state}%2C+USA"


def get_price():
    pass


def get_property_taxes():
    if True:
        pass
    else:
        pass
    pass  # If taxes not on zillow, use county office


def get_num_units():
    pass


def get_rent_per_unit():
    pass
