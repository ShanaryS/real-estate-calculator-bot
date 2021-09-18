"""Web scrapes current interest rates from 'https://www.nerdwallet.com/mortgages/mortgage-rates'."""


from bs4 import BeautifulSoup
import requests


def get_current_interest_rates() -> dict:
    """Returns web scraped current interest rates"""

    url = 'https://www.nerdwallet.com/mortgages/mortgage-rates'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    table = doc.find('tbody')

    interest_rates = {}
    for index, tr in enumerate(table.find_all('tr')):
        loan_type = tr.find('th').string
        rate = float(str(tr.find('td').string).split('%')[0]) / 100
        interest_rates[loan_type] = rate

    return interest_rates
