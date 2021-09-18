"""Web scrapes property info from zillow.com and countyoffice.org/tax-records/ for property taxes if necessary."""


from bs4 import BeautifulSoup
import requests


url = 'zillow.com'
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')


def get_price():
    pass


def get_property_taxes():
    pass  # If taxes not on zillow, use county office


def get_num_units():
    pass


def get_rent_per_unit():
    pass
