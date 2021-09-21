"""Web scrapes properties from zillow search URL."""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time


PROPERTIES_PER_PAGE = 40  # Number of properties zillow displays per search page
DRIVER_DELAY = 0.05  # Delay between actions for selenium driver
url_search: str
chrome: webdriver.Chrome
zillow: BeautifulSoup


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


def set_page_search(url) -> None:
    """Opens chromedriver using selenium"""

    global url_search, chrome, zillow

    url_search = _set_url_search(url)

    chrome = webdriver.Chrome()
    chrome.get(url_search)
    _scroll_to_page_bottom()

    # Creates beautiful soup object
    zillow_page = chrome.page_source
    zillow = BeautifulSoup(zillow_page, 'html.parser')


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


def _scroll_to_page_bottom() -> None:
    """Runs chrome browser with selenium and scrolls to bottom of page to load all JS elements"""

    time.sleep(1)  # Give time for the page to fully load. Though it should without, being cautious.

    # Handles zillow captcha that sometimes appear
    # Use this url to test captcha
    # chrome.get('https://www.zillow.com/captchaPerimeterX/?url=%2fhomes%2fCT_rb%2f&uuid=dd265dba-1ac2-11ec-a883-615050666d69&vid=')
    if 'captcha' in chrome.current_url.lower():

        target = chrome.find_element_by_id('px-captcha')
        action = webdriver.ActionChains(chrome)
        action.click_and_hold(on_element=target)
        action.perform()
        time.sleep(5)  # Holds button for 5 seconds. Should cover all the variable lengths

        action.release(on_element=target)
        action.perform()
        time.sleep(10)  # Wait for redirect from captcha. Can some times be long.

    target = chrome.find_element_by_tag_name("body")
    for i in range(10):
        target.send_keys(Keys.PAGE_DOWN)
        time.sleep(DRIVER_DELAY)


def get_url() -> str:
    """Returns URL for property"""
    return url_search


def _get_current_page(url) -> int:
    """Checks url to find current page"""

    if 'currentpage' not in url.lower():
        current_page_num = 1
    else:
        current_page_num = int(url.split('/')[4].split('_')[0])

    return current_page_num


def _set_url_to_first_page(url) -> str:
    """Makes sure that the url given starts on first page"""

    current_page_num = _get_current_page(url)

    if current_page_num == 1:
        first_page_url = url
    else:
        temp = url.split('/')
        temp.pop(4)
        temp[4] = temp[4].replace(f'%22pagination%22%3A%7B%22currentPage%22%3A{current_page_num}%7D%2C', '')
        first_page_url = '/'.join(temp)

    return first_page_url


def _get_num_pages_and_listings() -> tuple:
    """Returns the number of pages in the search"""

    # Checks if looking at agent listings or other listings. Other listings will always have 'cat2' in url.
    if 'cat2' not in url_search:
        listings = int(zillow.find_all(class_="total-text")[0].string.replace(',', ''))
        num_pages = -(-listings // PROPERTIES_PER_PAGE)  # Ceiling division
    else:
        listings = int(zillow.find_all(class_="total-text")[1].string.replace(',', ''))
        num_pages = -(-listings // PROPERTIES_PER_PAGE)  # Ceiling division

    return num_pages, listings


def _get_url_for_next_page(url) -> str:
    """Gets the url for the next page. Only for pages 2+"""

    current_page_num = _get_current_page(url)

    if current_page_num == 1:
        temp = url.splt('/')
        temp.insert(4, '2_p')
        temp[5] = temp[5].replace('%7B', '%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C')
    else:
        temp = url.split('/')
        temp[4] = f'{current_page_num + 1}_p'
        temp[5] = temp[5].replace(
            f"currentPage%22%3A{current_page_num}%7D%2C", f"currentPage%22%3A{current_page_num + 1}%7D%2C")

    next_page_url = '/'.join(temp)

    return next_page_url


def _get_property_url_from_search(li) -> str:
    """Gets url for property from search url"""

    property_url = li.find('a', href=True)['href']

    return property_url


def _get_price_from_search(li) -> int:
    """Gets price for property from search url"""

    price = int(li.find('div', class_="list-card-price").string.lstrip('$').replace(',', ''))

    return price


def get_all_urls_and_prices() -> dict:
    """Gets urls and prices for all properties on a zillow search page"""

    _scroll_to_page_bottom()

    base = zillow.find('div', id="grid-search-results").find('ul')

    properties_url_price = {}
    for li in base.contents:
        if li.find('div', id="nav-ad-container"):
            continue
        properties_url_price[_get_property_url_from_search(li)] = _get_price_from_search(li)

    return properties_url_price

# print(get_all_urls_and_prices('https://www.zillow.com/homes/CT_rb/'))
