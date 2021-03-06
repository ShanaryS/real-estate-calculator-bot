"""Web scrapes properties from zillow search URL."""

import bs4.element
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from dataclasses import dataclass

# Delay between actions for selenium driver
SCROLL_DELAY = 0.05
PAGE_LOAD_WAIT = 1
CAPTCHA_LOAD_WAIT = 1
HOLD_LENGTH = 11
REDIRECT_WAIT = 10

PROPERTIES_PER_PAGE = 40  # Number of properties zillow displays per search page


@dataclass
class SearchPage:
    """Stores info retrieved from the search page"""
    url_search: str
    chrome: webdriver.Chrome
    zillow: BeautifulSoup
    extra: int  # Sometimes urls have an extra '/' at the end.


def get_all_urls(url) -> list:
    """Gets urls and prices for all properties on a zillow search page"""

    _url_has_extra_slash(url)
    current_page_num = _get_current_page(url)
    SearchPage.url_search = _set_url_to_first_page(url, current_page_num)
    url = SearchPage.url_search

    _open_chrome(url)

    if 'captcha' in SearchPage.chrome.current_url.lower():
        _solve_captcha()

    _set_page_search()

    num_pages, num_listings = _get_num_pages_and_listings(url)
    num_pages = num_pages if num_pages < 30 else 30

    property_urls = []
    for page in range(1, num_pages+1):

        if 'captcha' in SearchPage.chrome.current_url.lower():
            _solve_captcha()

        _scroll_to_page_bottom()

        _set_page_search()
        base = SearchPage.zillow.find(
            'div', id="grid-search-results").find('ul')

        for li in base.contents:
            if li.find('div', id="nav-ad-container"):
                continue
            if _is_auction(li):
                continue
            property_urls.append(_get_property_url_from_search(li))

        if page < num_pages:
            url = _get_url_for_next_page(url, page)
            SearchPage.chrome.get(url)
            curr_url = SearchPage.chrome.current_url
            if curr_url != url and 'captcha' not in curr_url.lower():
                break

    SearchPage.chrome.quit()

    return property_urls


def is_url_valid(url) -> bool:
    """Checks if URL was incorrectly inputted by looking for an error page.
    For both individual properties and search
    """

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
        zillow_page = s.get(url, headers=req_headers).text

    # Creates beautiful soup object
    temp = BeautifulSoup(zillow_page, 'html.parser')

    valid = False if temp.find(id="zillow-error-page") else True

    try:
        valid_2 = True if 'auction' not in \
                           temp.find('div', class_="ds-home-details-chip"
                                     ).contents[2].text.lower() else False
    except AttributeError:
        valid_2 = True

    return all([valid, valid_2])


def _open_chrome(url) -> None:
    """Opens chromedriver using selenium"""

    SearchPage.chrome = webdriver.Chrome()
    SearchPage.chrome.get(url)


def _set_page_search() -> None:
    """Opens chromedriver using selenium"""

    # Creates beautiful soup object
    zillow_page = SearchPage.chrome.page_source
    SearchPage.zillow = BeautifulSoup(zillow_page, 'html.parser')


def _scroll_to_page_bottom() -> None:
    """Runs chrome browser with selenium to load all JS elements"""

    time.sleep(PAGE_LOAD_WAIT)  # Give time for the page to fully load.

    # Presses page down multiple times to scroll to bottom of page.
    target = SearchPage.chrome.find_element_by_tag_name("body")
    for i in range(10):
        target.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_DELAY)


def _solve_captcha() -> None:
    """Solves the captcha that sometimes appear.
    Use this url to test captcha:chrome.get(
    'https://www.zillow.com/captchaPerimeterX/
    ?url=%2fhomes%2fCT_rb%2f&uuid=dd265dba-1ac2-11ec-a883-615050666d69&vid=')
    """

    time.sleep(CAPTCHA_LOAD_WAIT)

    target = SearchPage.chrome.find_element_by_id('px-captcha')
    action = webdriver.ActionChains(SearchPage.chrome)
    action.click_and_hold(on_element=target)
    action.perform()
    time.sleep(HOLD_LENGTH)  # Holds button for HOLD_LENGTH seconds.

    action.release(on_element=target)
    action.perform()
    time.sleep(REDIRECT_WAIT)  # Wait for redirect from captcha.


def _set_url_to_first_page(url, current_page_num) -> str:
    """Makes sure that the url given starts on first page"""

    temp = url.split('/')
    if current_page_num > 1:
        temp.pop(-2 - SearchPage.extra)
    if _currentpage_is_last(url):
        temp[-1 - SearchPage.extra] = _rreplace(
            temp[-1 - SearchPage.extra],
            f"%2C%22pagination%22%3A%7B%22currentPage%22%3A"
            f"{current_page_num}%7D%7D", '%7D', 1)
    else:
        temp[-1 - SearchPage.extra] = temp[-1 - SearchPage.extra].replace(
            f'%22pagination%22%3A%7B%22currentPage%22%3A'
            f'{current_page_num}%7D%2C', '')
    first_page_url = '/'.join(temp)

    return first_page_url


def _get_current_page(url) -> int:
    """Checks url to find current page"""

    if 'currentpage' not in url.lower():
        current_page_num = 1
    else:
        current_page_num = int(
            url.split('/')[-2 - SearchPage.extra].split('_')[0])

    return current_page_num


def _currentpage_is_last(url) -> bool:
    """Checks if current page is last in url"""

    if len(url) - url.lower().find('currentpage') < 30:
        return True
    return False


def _url_has_extra_slash(url) -> None:
    """Checks if URL has extra / which other functions need to compensate for"""

    if url.endswith('/'):
        SearchPage.extra = 1
    else:
        SearchPage.extra = 0


def _get_num_pages_and_listings(url) -> tuple:
    """Returns the number of pages in the search"""

    # Other listings will always have 'cat2' in url.
    if 'cat2' not in url:
        num_listings = int(SearchPage.zillow.find_all(
            class_="total-text")[0].string.replace(',', ''))
        num_pages = -(-num_listings // PROPERTIES_PER_PAGE)  # Ceiling division
    else:
        num_listings = int(SearchPage.zillow.find_all(
            class_="total-text")[1].string.replace(',', ''))
        num_pages = -(-num_listings // PROPERTIES_PER_PAGE)  # Ceiling division

    return num_pages, num_listings


def _rreplace(s, old, new, occurrence):
    """Replaces last occurrence of string"""

    a = s.rsplit(old, occurrence)
    return new.join(a)


def _get_url_for_next_page(url, current_page_num) -> str:
    """Gets the url for the next page. Only for pages 2+"""

    if current_page_num == 1:
        temp = url.split('/')
        temp.insert(-1 - SearchPage.extra, '2_p')
        if _currentpage_is_last(url):
            temp[-1 - SearchPage.extra] = _rreplace(
                temp[-1 - SearchPage.extra], '%7D',
                '%2C%22pagination%22%3A%7B%22currentPage%22%3A2%7D%7D', 1)
        else:
            temp[-1 - SearchPage.extra] = temp[-1 - SearchPage.extra].replace(
                '%7B',
                '%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C', 1)
    else:
        temp = url.split('/')
        temp[-2 - SearchPage.extra] = f'{current_page_num + 1}_p'
        if _currentpage_is_last(url):
            temp[-1 - SearchPage.extra] = _rreplace(
                temp[-1 - SearchPage.extra],
                f"currentPage%22%3A{current_page_num}%7D%7D",
                f"currentPage%22%3A{current_page_num + 1}%7D%7D", 1)
        else:
            temp[-1 - SearchPage.extra] = temp[-1 - SearchPage.extra].replace(
                f"currentPage%22%3A{current_page_num}%7D%2C",
                f"currentPage%22%3A{current_page_num + 1}%7D%2C")

    next_page_url = '/'.join(temp)

    return next_page_url


def _is_auction(li: bs4.element.Tag) -> bool:
    """Checks if house is an auction"""

    try:
        is_auction = False if 'auction' not in li.find(
            'li', class_="list-card-statusText").text.lower() else True
    except AttributeError:
        is_auction = False

    return is_auction


def _get_property_url_from_search(li: bs4.element.Tag) -> str:
    """Gets url for property from search url"""

    property_url = li.find('a', href=True)['href']

    return property_url


# Currently not used. No reason to delete however.
def _get_price_from_search(li: bs4.element.Tag) -> int:
    """Gets price for property from search url"""

    price = int(li.find(
        'div', class_="list-card-price").string.lstrip('$').replace(',', ''))

    return price
