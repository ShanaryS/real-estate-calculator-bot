"""Web scrapes properties from zillow search URL."""


from bs4 import BeautifulSoup
import requests


url_search: str
zillow: BeautifulSoup
page: requests.Session()


def _set_url_search(url) -> str:
    """Gets zillow search URL from user or file when running analysis"""

    if url:
        _url = url
    else:
        _url = str(input("Enter full URL from zillow search: "))

    while _url[:23] != 'https://www.zillow.com/' or len(_url) < 29:
        _url = str(input("Enter full URL from zillow search: "))
    print()

    return _url


def set_page_search(url) -> None:
    """Gets html page to parse"""

    global url_search, zillow, page

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
        url_property = _set_url_search(url)
        zillow_page = s.get(url_property, headers=req_headers).text
        page = zillow_page  # Hoping this reduces unnecessary calls to zillow for certain functions

    # Creates beautiful soup object
    zillow = BeautifulSoup(zillow_page, 'html.parser')


def get_url() -> str:
    """Returns URL for property"""
    return url_search


def get_property_url() -> str:
    """Gets url for property from search url"""


def get_price() -> int:
    """Gets price for property from search url"""
