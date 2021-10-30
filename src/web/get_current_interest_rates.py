"""Web scrapes current interest rates.
Uses 'https://www.nerdwallet.com/mortgages/mortgage-rates'.
"""

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from src.data.colors_for_print import OK, END


@dataclass
class InterestRates:
    """Stores current interest rates scraped from the web"""
    interest_rates = {}


def set_page_interest_rates() -> None:
    """Get page and stores interest rates. Only ran once the per session."""

    print(f"{OK}--- Getting current interest rates...{END}\n")

    url = 'https://www.nerdwallet.com/mortgages/mortgage-rates'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    table = doc.find('tbody')

    for tr in table.find_all('tr'):
        loan_type = tr.find('th').string
        rate = float(str(tr.find('td').string).split('%')[0]) / 100
        InterestRates.interest_rates[loan_type] = rate
