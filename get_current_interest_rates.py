"""Web scrapes current interest rates from 'https://www.nerdwallet.com/mortgages/mortgage-rates'."""


from bs4 import BeautifulSoup
import requests


interest_rates = {}


def set_page_interest_rates() -> None:
    """Get page and stores interest rates"""

    url = 'https://www.nerdwallet.com/mortgages/mortgage-rates'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    table = doc.find('tbody')

    for index, tr in enumerate(table.find_all('tr')):
        loan_type = tr.find('th').string
        rate = float(str(tr.find('td').string).split('%')[0]) / 100
        interest_rates[loan_type] = rate
