from bs4 import BeautifulSoup
import requests


url_search: str
zillow: BeautifulSoup
page: requests.Session()


def _set_url_search() -> str:
    """Gets zillow search url from user or file when running analysis"""

    url = str(input("Enter full url from zillow search: "))

    while url[:23] != 'https://www.zillow.com/' or len(url) < 31:
        url = str(input("Enter full url from zillow search: "))
    print()

    return url


def set_page_search() -> None:
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
        url_property = _set_url_search()
        zillow_page = s.get(url_property, headers=req_headers).text
        page = zillow_page  # Hoping this reduces unnecessary calls to zillow for certain functions

    # Creates beautiful soup object
    zillow = BeautifulSoup(zillow_page, 'html.parser')


def get_links() -> list:
    """"""

    return list of links to use indivdually
