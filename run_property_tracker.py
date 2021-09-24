"""Use before run_analysis.py to choose urls. Can add property urls or search urls."""


import os.path
import json
import time
from dataclasses import dataclass
from data.calculations import save_urls
from data.user import get_url_from_input
from data.colors_for_print import PrintColors
from web.get_property_urls_from_search import is_url_valid, get_all_urls


# Used for delaying terminating program so user can read final text
EXIT_TIMER = 1
DELAY_TO_GET_URLS = 5

# Use for navigating through menus
S_P_R, SEARCH, PROPERTY, REFRESH, A_O_D = 's_p_r', 's', 'p', 'r', 'a_o_d'
APPEND, OVERWRITE, DELETE, CANCEL, EXECUTE = 'a', 'o', 'd', 'c', 'e'


@dataclass
class State:
    """Saves the state of the user choices"""
    is_search = to_overwrite = to_delete = False
    urls = set()


def _quit_program() -> None:
    """Quits programing without saving an data"""

    _print_captions(mode=CANCEL)
    time.sleep(EXIT_TIMER)


def _url_is_valid(url_test) -> bool:
    """Checks if URL is valid"""

    # If user is deleting URL, no need to verify
    if State.to_delete:
        return True

    _print_captions(verifying_url=True)

    # If not zillow URL, return false
    if url_test[:23] != 'https://www.zillow.com/' or len(url_test) <= 29:
        return False

    # Handles special case of search url
    if url_test[:28] == 'https://www.zillow.com/homes':
        if not State.is_search:
            return False

    # Search page filters are only stored in URLs when they are 100+ characters.
    # This prevents URLs with less from being added.
    # Any search URL that has less than 800 listings (a hard requirement),
    # will have enough characters to never be affected by this.
    if len(url_test) < 100 and State.is_search:
        return False

    # Sends a get request to see if page returns an error. As well as check if property is an auction.
    if not is_url_valid(url_test):
        return False

    return True


def _commit_updates_to_file() -> None:
    """Commits changes to file"""

    if State.urls:
        save_urls(State.urls, overwrite=State.to_overwrite, search=State.is_search, delete=State.to_delete)

    if State.is_search and not State.to_delete:
        _print_captions(execute_s=True)
        time.sleep(DELAY_TO_GET_URLS)
        _get_urls_from_search()

    _print_captions(execute=True)
    time.sleep(EXIT_TIMER)


def _print_captions(mode=None, e=False, verifying_url=False, valid=True,
                    received=False, execute_s=False, execute=False, search_limitations=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    BAD, OK, GOOD, GREAT = PrintColors.FAIL, PrintColors.WARNING, PrintColors.OKCYAN, PrintColors.OKGREEN
    END = PrintColors.ENDC

    if mode == 's_p_r':
        print(f"{GOOD}Do you want to update Search URLs '{GREAT}s{GOOD}', update Property URLs '{GREAT}p{GOOD}', "
              f"or refresh Search URLs '{GREAT}r{GOOD}'? ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == 'a_o_d':
        print(f"{GOOD}Do you want to append '{GREAT}a{GOOD}', overwrite '{GREAT}o{GOOD}', or delete '{GREAT}d{GOOD}'? "
              f"('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == 'a':
        print(f"\n{OK}--- APPEND MODE... URLs in this session will be appended to file! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to append ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}- Enter URL to append ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == 'o':
        print(f"\n{OK}--- OVERWRITE MODE... URLs before this session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to write ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to write ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == 'd':
        print(f"\n{OK}--- DELETE MODE... URLs in session will be removed! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to delete ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to delete ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == 'c':
        print(f"\n{BAD}!!! No changes were made! Ending program... !!!{END}")

    elif verifying_url:
        print(f"\n{OK}... Verifying URL ...{END}")
    elif not valid:
        print(f"\n{BAD}!!! Invalid URL... Correct URL for Search/Property? - For Searches try setting a price range. "
              f"For property analysis auctions are not allowed.   !!!{END}")
    elif received:
        print(f"\n{GREAT}!!! URL received! !!!{END}")
    elif execute_s:
        print(f"\n{OK}!!! WILL START GETTING PROPERTY URLs FROM SEARCH URLs IN: {GOOD}{DELAY_TO_GET_URLS}s{OK} !!!{END}"
              f"\n{OK}!!! Expected Duration: {GOOD}10s{OK} PER {GOOD}100{OK} LISTINGS IN SEARCH URLs! !!!{END}"
              f"\n{BAD}!!! DO NOT TOUCH ANYTHING. IT MAY PAUSE FOR UP TO {GOOD}10s{BAD}. THIS IS NORMAL. !!!{END}")
    elif execute:
        print(f"\n{GREAT}!!! Committed changes to file! Ending program... !!!{END}")
    elif search_limitations:
        print(f"\n\n{BAD}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
              f"Zillow only displays 800 properties per search. If listings is above 800, certain properties\n"
              f"CANNOT be accessed. Instead, filter number of listings heavily to make sure it does not\n"
              f"exceed 800. Split the search criteria into multiple separate searches.\n\n"
              
              f"{OK}For example: Instead of a single URL with a price range of $100k-$1M, use two URLs with price\n"
              f"ranges of $100k-$500k and $500k-$1M. Assuming each of those searches return less than 800 listings.\n"
              f"P.S 'Agent' listing URLs doesn't include 'Other' properties. Add both URLs to include all properties.\n"
              f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{END}\n")


def add_link(mode=None, refresh_no_input=False) -> None:
    """Logic for adding URLs"""

    if refresh_no_input:
        State.is_search = True
        _commit_updates_to_file()
        return

    _print_captions(mode=mode)
    search_property_update = input()
    while search_property_update != SEARCH and search_property_update != PROPERTY \
            and search_property_update != REFRESH and search_property_update != CANCEL:
        _print_captions(mode=mode)
        search_property_update = input()

    if search_property_update != CANCEL:
        if search_property_update == SEARCH:
            _print_captions(search_limitations=True)
            State.is_search = True
            _choose_options(A_O_D)
        elif search_property_update == PROPERTY:
            State.is_search = False
            _choose_options(A_O_D)
        elif search_property_update == REFRESH:
            State.is_search = True
            _commit_updates_to_file()
    elif search_property_update == CANCEL:
        _quit_program()
        return


def _choose_options(mode) -> None:
    """Handles the user choosing different options for URLs"""

    _print_captions(mode=mode)
    append_overwrite_delete = input()
    while append_overwrite_delete != APPEND and append_overwrite_delete != OVERWRITE \
            and append_overwrite_delete != DELETE and append_overwrite_delete != CANCEL:
        _print_captions(mode=mode)
        append_overwrite_delete = input()

    if append_overwrite_delete != CANCEL:
        if append_overwrite_delete == APPEND:
            _get_urls_from_input(APPEND)
        elif append_overwrite_delete == OVERWRITE:
            State.to_overwrite = True
            _get_urls_from_input(OVERWRITE)
        elif append_overwrite_delete == DELETE:
            State.to_delete = True
            _get_urls_from_input(DELETE)
    elif append_overwrite_delete == CANCEL:
        _quit_program()
        return


def _get_urls_from_input(mode) -> None:
    """Gets URLs from user. Calls functions that adds them to file"""

    _print_captions(mode=mode)
    new_url = get_url_from_input()

    if new_url != CANCEL:
        valid = _url_is_valid(new_url)
        while not valid:
            _print_captions(valid=False)

            _print_captions(mode=mode)
            new_url = get_url_from_input()

            if new_url == CANCEL:
                _quit_program()
                return

            valid = _url_is_valid(new_url)

        State.urls.add(new_url)
        _print_captions(received=True)

        _print_captions(mode=mode, e=True)
        new_url = get_url_from_input()
        while new_url != CANCEL:

            if new_url == EXECUTE:
                _commit_updates_to_file()
                return

            else:
                valid = _url_is_valid(new_url)
                while not valid:
                    _print_captions(valid=False)

                    _print_captions(mode=mode, e=True)
                    new_url = get_url_from_input()

                    if new_url == EXECUTE:
                        _commit_updates_to_file()
                        return

                    if new_url == CANCEL:
                        _quit_program()
                        return

                    valid = _url_is_valid(new_url)

                State.urls.add(new_url)
                _print_captions(received=True)

            _print_captions(mode=mode, e=True)
            new_url = get_url_from_input()

        if new_url == CANCEL:
            _quit_program()
            return

    elif new_url == CANCEL:
        _quit_program()
        return


def _get_urls_from_search() -> None:
    """Get the property urls from the search url"""

    try:
        with open(os.path.join('output', 'urls.json')) as json_file:
            urls_json = json.load(json_file)

        # Get property URLs for each Search URL and place them under their respective Search URL.
        # Coverts result list -> set -> list to remove any potential duplicates. Should be none but don't want any
        # chance of making redundant get request for the analysis.
        for search_url in urls_json.setdefault('Search', dict()):

            # Gets all URLs from the search link. Any duplicate properties compared to urls in 'Property' in urls.json
            # is removed. This way if user deletes a specific property to track, the analysis of that property
            # can be easily deleted as well.
            urls_search = set(get_all_urls(search_url))
            urls_properties = set(urls_json.get('Property', set()))
            urls_search.difference_update(urls_properties)

            # Converts urls_search back to list to add to json. It does not accept sets.
            urls_json['Search'][search_url] = list(urls_search)

        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump(urls_json, json_file, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump({'Search': {}, 'Property': {}}, json_file, indent=4)


if __name__ == '__main__':
    add_link(mode=S_P_R)
