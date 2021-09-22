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
        valid_2 = False if 'auction' in \
                           zillow.find('div', class_="ds-home-details-chip").contents[2].text.lower() else True
    except AttributeError:
        valid_2 = True

    return all([valid, valid_2])


def get_url() -> str:
    """Returns URL for property"""
    return url_search


def set_page_search(url) -> None:
    """Opens chromedriver using selenium"""

    global url_search, chrome, zillow

    url_search = url

    chrome = webdriver.Chrome()
    chrome.get(url_search)

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


def _set_url_to_first_page(current_page_num) -> str:
    """Makes sure that the url given starts on first page"""

    temp = url_search.split('/')
    temp.pop(-2 - extra)
    if _currentpage_is_last(url_search):
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
        temp.insert(-2 - extra, '2_p')
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
        valid = False if 'auction' not in li.find('li', class_="list-card-statusText").text.lower() else True
    except AttributeError:
        valid = True

    return valid


def _get_property_url_from_search(li: bs4.element.Tag) -> str:
    """Gets url for property from search url"""

    property_url = li.find('a', href=True)['href']

    return property_url


def _get_price_from_search(li: bs4.element.Tag) -> int:
    """Gets price for property from search url"""

    price = int(li.find('div', class_="list-card-price").string.lstrip('$').replace(',', ''))

    return price


def get_all_urls_and_prices(url) -> dict:
    """Gets urls and prices for all properties on a zillow search page"""

    set_page_search(url)

    if 'captcha' in chrome.current_url.lower():
        _solve_captcha()

    _url_has_extra_slash(url_search)

    current_page_num = _get_current_page(url_search)

    if current_page_num != 1:
        url = _set_url_to_first_page(current_page_num)
    else:
        url = url_search

    num_pages, num_listings = _get_num_pages_and_listings(url)

    properties_url_price = {}
    for page in range(1, num_pages+1):
        if 'captcha' in chrome.current_url.lower():
            _solve_captcha()

        _scroll_to_page_bottom()

        base = zillow.find('div', id="grid-search-results").find('ul')

        for li in base.contents:
            if li.find('div', id="nav-ad-container"):
                continue
            if _is_auction(li):
                continue
            print(_get_property_url_from_search(li), _get_price_from_search(li))
            properties_url_price[_get_property_url_from_search(li)] = _get_price_from_search(li)

        url = _get_url_for_next_page(url, page)
        chrome.get(url)

    return properties_url_price

test = 'https://www.zillow.com/ct/9_p/?searchQueryState=%7B%22usersSearchTerm%22%3A%22CT%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.36425648828126%2C%22east%22%3A-71.15075551171876%2C%22south%22%3A40.66259092879424%2C%22north%22%3A42.33283762638384%7D%2C%22mapZoom%22%3A9%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A11%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22category%22%3A%22cat2%22%2C%22pagination%22%3A%7B%22currentPage%22%3A9%7D%7D'
test2 = 'https://www.zillow.com/waterbury-ct/duplex/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-73.12574140551757%2C%22east%22%3A-72.92489759448242%2C%22south%22%3A41.51236007362086%2C%22north%22%3A41.61665220271312%7D%2C%22mapZoom%22%3A13%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A34671%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A250000%7D%2C%22beds%22%3A%7B%22min%22%3A0%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22sch%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A1250%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Atrue%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
test3 = 'https://www.zillow.com/ct/13_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A13%7D%2C%22usersSearchTerm%22%3A%22CT%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.36425648828126%2C%22east%22%3A-71.15075551171876%2C%22south%22%3A40.66259092879424%2C%22north%22%3A42.33283762638384%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A11%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%7D'
captcha = 'https://www.zillow.com/captchaPerimeterX/?url=%2fhomes%2fCT_rb%2f&uuid=dd265dba-1ac2-11ec-a883-615050666d69&vid='
print(get_all_urls_and_prices(captcha))
