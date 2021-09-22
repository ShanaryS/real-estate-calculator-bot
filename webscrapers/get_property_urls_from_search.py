"""Web scrapes properties from zillow search URL."""
import bs4.element
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time


# Delay between actions for selenium driver
SCROLL_DELAY = 0.05
PAGE_LOAD_WAIT = 1
CAPTCHA_LOAD_WAIT = 1
HOLD_LENGTH = 5
REDIRECT_WAIT = 10

PROPERTIES_PER_PAGE = 40  # Number of properties zillow displays per search page

# Global variables all functions use
url_search: str
chrome: webdriver.Chrome
zillow: BeautifulSoup
extra: int  # Sometimes urls have an extra '/' at the end. This accounts for it


def is_url_valid(url) -> bool:
    """Checks if URL was incorrectly inputted by looking for an error page. For both individual properties and search"""

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

    try:
        valid_2 = True if 'auction' not in \
                           temp.find('div', class_="ds-home-details-chip").contents[2].text.lower() else False
    except AttributeError:
        valid_2 = True

    return all([valid, valid_2])


def get_url() -> str:
    """Returns URL for property"""
    return url_search


def open_chrome(url) -> None:
    """Opens chromedriver using selenium"""

    global chrome

    chrome = webdriver.Chrome()
    chrome.get(url)


def set_page_search() -> None:
    """Opens chromedriver using selenium"""

    global zillow

    # Creates beautiful soup object
    zillow_page = chrome.page_source
    zillow = BeautifulSoup(zillow_page, 'html.parser')


def _scroll_to_page_bottom() -> None:
    """Runs chrome browser with selenium and scrolls to bottom of page to load all JS elements"""

    time.sleep(PAGE_LOAD_WAIT)  # Give time for the page to fully load. Though it should without, being cautious.

    # Presses page down multiple times to scroll to bottom of page.
    target = chrome.find_element_by_tag_name("body")
    for i in range(10):
        target.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_DELAY)


def _solve_captcha() -> None:
    """Solves the captcha that sometimes appear.
    Use this url to test captcha:chrome.get(
    'https://www.zillow.com/captchaPerimeterX/?url=%2fhomes%2fCT_rb%2f&uuid=dd265dba-1ac2-11ec-a883-615050666d69&vid=')
    """

    time.sleep(CAPTCHA_LOAD_WAIT)

    target = chrome.find_element_by_id('px-captcha')
    action = webdriver.ActionChains(chrome)
    action.click_and_hold(on_element=target)
    action.perform()
    time.sleep(HOLD_LENGTH)  # Holds button for 5 seconds. Should cover all the variable lengths

    action.release(on_element=target)
    action.perform()
    time.sleep(REDIRECT_WAIT)  # Wait for redirect from captcha. Can some times be long.


def _set_url_to_first_page(url, current_page_num) -> str:
    """Makes sure that the url given starts on first page"""

    temp = url.split('/')
    temp.pop(-2 - extra)
    if _currentpage_is_last(url):
        temp[-1 - extra] = _rreplace(
            temp[-1 - extra], f"%2C%22pagination%22%3A%7B%22currentPage%22%3A{current_page_num}%7D%7D", '%7D', 1)
    else:
        temp[-1 - extra] = temp[-1 - extra].replace(
            f'%22pagination%22%3A%7B%22currentPage%22%3A{current_page_num}%7D%2C', '')
    first_page_url = '/'.join(temp)

    return first_page_url


def _get_current_page(url) -> int:
    """Checks url to find current page"""

    if 'currentpage' not in url.lower():
        current_page_num = 1
    else:
        current_page_num = int(url.split('/')[-2 - extra].split('_')[0])

    return current_page_num


def _currentpage_is_last(url) -> bool:
    """Checks if current page is last in url"""

    if len(url) - url.lower().find('currentpage') < 30:
        return True
    return False


def _url_has_extra_slash(url) -> None:
    """Checks if URL has extra / which other functions need to compensate for"""

    global extra

    if url.endswith('/'):
        extra = 1
    else:
        extra = 0


def _get_num_pages_and_listings(url) -> tuple:
    """Returns the number of pages in the search"""

    # Checks if looking at Agent listings or Other listings. Other listings will always have 'cat2' in url.
    if 'cat2' not in url:
        num_listings = int(zillow.find_all(class_="total-text")[0].string.replace(',', ''))
        num_pages = -(-num_listings // PROPERTIES_PER_PAGE)  # Ceiling division
    else:
        num_listings = int(zillow.find_all(class_="total-text")[1].string.replace(',', ''))
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
        temp.insert(-1 - extra, '2_p')
        if _currentpage_is_last(url):
            temp[-1 - extra] = _rreplace(
                temp[-1 - extra], '%7D', '%2C%22pagination%22%3A%7B%22currentPage%22%3A2%7D%7D', 1)
        else:
            temp[-1 - extra] = temp[-1 - extra].replace(
                '%7B', '%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C', 1)
    else:
        temp = url.split('/')
        temp[-2 - extra] = f'{current_page_num + 1}_p'
        if _currentpage_is_last(url):
            temp[-1 - extra] = _rreplace(
                temp[-1 - extra],
                f"currentPage%22%3A{current_page_num}%7D%7D", f"currentPage%22%3A{current_page_num + 1}%7D%7D", 1)
        else:
            temp[-1 - extra] = temp[-1 - extra].replace(
                f"currentPage%22%3A{current_page_num}%7D%2C", f"currentPage%22%3A{current_page_num + 1}%7D%2C")

    next_page_url = '/'.join(temp)

    return next_page_url


def _is_auction(li: bs4.element.Tag) -> bool:
    """Checks if house is an auction"""

    try:
        is_auction = False if 'auction' not in li.find('li', class_="list-card-statusText").text.lower() else True
    except AttributeError:
        is_auction = False

    return is_auction


def _get_property_url_from_search(li: bs4.element.Tag) -> str:
    """Gets url for property from search url"""

    property_url = li.find('a', href=True)['href']

    return property_url


def _get_price_from_search(li: bs4.element.Tag) -> int:
    """Gets price for property from search url"""

    price = int(li.find('div', class_="list-card-price").string.lstrip('$').replace(',', ''))

    return price


def get_all_urls_and_prices(url) -> dict:
    """Main function to call. Gets urls and prices for all properties on a zillow search page"""

    global zillow, url_search

    _url_has_extra_slash(url)
    current_page_num = _get_current_page(url)
    url_search = _set_url_to_first_page(url, current_page_num)
    url = url_search

    open_chrome(url)
    set_page_search()

    if 'captcha' in chrome.current_url.lower():
        _solve_captcha()

    num_pages, num_listings = _get_num_pages_and_listings(url)

    properties_url_price = {}
    for page in range(1, num_pages+1):

        if 'captcha' in chrome.current_url.lower():
            _solve_captcha()

        _scroll_to_page_bottom()

        set_page_search()
        base = zillow.find('div', id="grid-search-results").find('ul')

        for li in base.contents:
            if li.find('div', id="nav-ad-container"):
                continue
            if _is_auction(li):
                continue
            properties_url_price[_get_property_url_from_search(li)] = _get_price_from_search(li)

        if page < num_pages:
            url = _get_url_for_next_page(url, page)
            chrome.get(url)
            curr_url = chrome.current_url
            if curr_url != url and 'captcha' not in curr_url.lower():  # If no more pages to go through
                break

    chrome.close()

    return properties_url_price
