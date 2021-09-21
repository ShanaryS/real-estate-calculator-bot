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
        url_search = _set_url_search(url)
        zillow_page = s.get(url_search, headers=req_headers).text
        page = zillow_page  # Hoping this reduces unnecessary calls to zillow for certain functions

    # Creates beautiful soup object
    zillow = BeautifulSoup(zillow_page, 'html.parser')


def is_url_valid(url) -> bool:
    """Checks if URL was incorrectly inputted by looking for an error page"""

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
        zillow_page = s.get(url, headers=req_headers).text

    # Creates beautiful soup object
    temp = BeautifulSoup(zillow_page, 'html.parser')

    valid = False if temp.find(id="zillow-error-page") else True

    return valid


def get_url() -> str:
    """Returns URL for property"""
    return url_search


def get_num_pages() -> int:
    """Returns the number of pages in the search"""

    PROPERTIES_PER_PAGE = 40  # Number of properties zillow displays per search page

    # Checks if looking at agent listings or other listings. Other listings will always have 'cat2' in url.
    if 'cat2' not in url_search:
        num_pages = int(zillow.find_all(class_="total-text")[0].string.replace(',', ''))
        num_pages = -(-num_pages // PROPERTIES_PER_PAGE)  # Ceiling division
    else:
        num_pages = int(zillow.find_all(class_="total-text")[1].string.replace(',', ''))
        num_pages = -(-num_pages // PROPERTIES_PER_PAGE)  # Ceiling division

    return num_pages


# def get_property_url_from_search() -> str:
#     """Gets url for property from search url"""
#
#     return property_url
#
#
# def get_price_from_search() -> int:
#     """Gets price for property from search url"""
#
#     return price
