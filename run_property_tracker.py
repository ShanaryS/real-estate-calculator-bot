"""Use before run_analysis.py to choose urls. Can add property urls or search urls."""

import os.path
import json
import time
from dataclasses import dataclass
from data.calculations import write_urls, write_urls_ignore
from data.user import get_url_from_input
from data.colors_for_print import BAD, OK, GOOD, GREAT, END
from web.get_property_urls_from_search import is_url_valid, get_all_urls

# Used for delaying terminating program so user can read final text
EXIT_TIMER = 2
DELAY_TO_GET_URLS = 5

# Use for navigating through menus
S_P_R_I, SEARCH, PROPERTY, REFRESH, IGNORE = 's_p_r_i', 's', 'p', 'r', 'i'
A_O_D, APPEND, OVERWRITE, DELETE, CANCEL, EXECUTE = 'a_o_d', 'a', 'o', 'd', 'c', 'e'


@dataclass
class State:
    """Saves the state of the user choices"""
    is_search = to_overwrite = to_delete = to_ignore = False
    search_property_refresh_ignore = {SEARCH, PROPERTY, REFRESH, IGNORE, CANCEL}
    append_overwrite_delete = {APPEND, OVERWRITE, DELETE, CANCEL}
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
        if State.to_ignore:
            write_urls_ignore(State.urls)
        else:
            write_urls(State.urls, overwrite=State.to_overwrite, search=State.is_search, delete=State.to_delete)

    if State.is_search and not State.to_delete:
        _print_captions(execute_s=True)
        time.sleep(DELAY_TO_GET_URLS)
        _get_urls_from_search()

    _print_captions(execute=True)
    time.sleep(EXIT_TIMER)


def _print_captions(mode=None, e=False, verifying_url=False, valid=True,
                    received=False, execute_s=False, execute=False, search_limitations=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    if mode == S_P_R_I:
        print(f"{GOOD}Do you want to update Search URLs '{GREAT}s{GOOD}', update Property URLs '{GREAT}p{GOOD}',\n"
              f"        refresh Search URLs '{GREAT}r{GOOD}' or ignore URLs '{GREAT}i{GOOD}'? "
              f"('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == A_O_D:
        print(f"{GOOD}Do you want to append '{GREAT}a{GOOD}', overwrite '{GREAT}o{GOOD}', or delete '{GREAT}d{GOOD}'? "
              f"('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == APPEND:
        print(f"\n{OK}--- APPEND MODE... URLs in this session will be appended to file! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to append ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}- Enter URL to append ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == OVERWRITE:
        print(f"\n{OK}--- OVERWRITE MODE... URLs before this session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to write ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to write ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == DELETE:
        print(f"\n{OK}--- DELETE MODE... URLs in session will be removed! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to delete ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to delete ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == IGNORE:
        print(f"\n{OK}--- IGNORE MODE... URLs in session will be ignored from analysis! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to ignore ('{GREAT}e{GOOD}' to execute changes, "
                  f"'{GREAT}c{GOOD}' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to ignore ('{GREAT}c{GOOD}' to cancel):{END}", end=" ")
    elif mode == CANCEL:
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

    # If refreshing urls from run_refresh_listings_and_analyses.py. Skips input.
    if refresh_no_input:
        State.is_search = True
        _commit_updates_to_file()
        return

    _print_captions(mode=mode)
    search_property_refresh_ignore = input()
    print()
    while search_property_refresh_ignore not in State.search_property_refresh_ignore:
        _print_captions(mode=mode)
        search_property_refresh_ignore = input()
        print()

    if search_property_refresh_ignore != CANCEL:
        if search_property_refresh_ignore == SEARCH:
            _print_captions(search_limitations=True)
            State.is_search = True
            _choose_options(A_O_D)
        elif search_property_refresh_ignore == PROPERTY:
            State.is_search = False
            _choose_options(A_O_D)
        elif search_property_refresh_ignore == REFRESH:
            State.is_search = True
            _commit_updates_to_file()
        elif search_property_refresh_ignore == IGNORE:
            State.to_ignore = True
            _get_urls_from_input(IGNORE)
    elif search_property_refresh_ignore == CANCEL:
        _quit_program()
        return


def _choose_options(mode) -> None:
    """Handles the user choosing different options for URLs"""

    _print_captions(mode=mode)
    append_overwrite_delete = input()
    print()
    while append_overwrite_delete not in State.append_overwrite_delete:
        _print_captions(mode=mode)
        append_overwrite_delete = input()
        print()

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
    print()

    if new_url != CANCEL:
        valid = _url_is_valid(new_url)
        while not valid:
            _print_captions(valid=False)

            _print_captions(mode=mode)
            new_url = get_url_from_input()
            print()

            if new_url == CANCEL:
                _quit_program()
                return

            valid = _url_is_valid(new_url)

        State.urls.add(new_url)
        _print_captions(received=True)

        _print_captions(mode=mode, e=True)
        new_url = get_url_from_input()
        print()
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
                    print()

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
            print()

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

        # Loads URLs that the user wants to ignore
        try:
            with open(os.path.join('output', 'ignored_urls.txt')) as txt_file:
                urls_txt = {url.strip() for url in txt_file.readlines()}
        except FileNotFoundError:
            urls_txt = set()

        # Get property URLs for each Search URL and place them under their respective Search URL.
        # Coverts result list -> set -> list to remove any potential duplicates. Should be none but don't want any
        # chance of making redundant get request for the analysis.
        for search_url in urls_json.setdefault('Search', dict()):

            # Gets all URLs from the search link. Any duplicate properties compared to urls in 'Property' in urls.json
            # is removed. This way if user deletes a specific property to track, the analysis of that property
            # can be easily deleted as well.
            urls_search = set(get_all_urls(search_url))
            urls_properties = set(urls_json.get('Property', set()))
            urls_search.difference_update(urls_properties)  # Subtracts property URLs from search property URLs.
            urls_search.difference_update(urls_txt)  # Subtracts ignored urls from urls to be saved.

            # Converts urls_search back to list to add to json. It does not accept sets.
            urls_json['Search'][search_url] = list(urls_search)

        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump(urls_json, json_file, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump({'Search': {}, 'Property': {}}, json_file, indent=4)


def main() -> None:
    """Main function"""

    add_link(mode=S_P_R_I)


if __name__ == '__main__':
    main()
