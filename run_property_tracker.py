"""Use before run_analysis.py to choose urls. Can add property urls or search urls."""


import os.path
import json
import time
from data.calculations import save_urls
from data.user import get_url_from_input
from data.colors_for_print import PrintColors
from web.get_property_urls_from_search import is_url_valid, get_all_urls_and_prices


# Stores the urls from inputs. Gets written to file after add_link() is completed. If was cancelled, it gets cleared.
urls = set()

# Variables that dictate how each option that the user chooses is handled
to_overwrite = is_search = to_delete = False
s_p_r, search, property_, refresh, a_o_d = 's_p_r', 's', 'p', 'r', 'a_o_d'
append, overwrite, delete, cancel, exe = 'a', 'o', 'd', 'c', 'e'

# Used for delaying terminating program so user can read final text
EXIT_TIMER = 1
DELAY_TO_GET_URLS = 5


def quit_program() -> None:
    """Quits programing without saving an data"""

    print_captions(mode=cancel)
    time.sleep(EXIT_TIMER)


def url_is_valid(url_test) -> bool:
    """Checks if URL is valid"""

    # If user is deleting URL, no need to verify
    if to_delete:
        return True

    print_captions(verifying_url=True)

    # If not zillow URL, return false
    if url_test[:23] != 'https://www.zillow.com/' or len(url_test) <= 29:
        return False

    # Handles special case of search url
    if url_test[:28] == 'https://www.zillow.com/homes':
        if not is_search:
            return False

    # Search page filters are only stored in URLs when they are 100+ characters.
    # This prevents URLs with less from being added.
    # Any search URL that has less than 800 listings (a hard requirement),
    # will have enough characters to never be affected by this.
    if len(url_test) < 100 and is_search:
        return False

    # Sends a get request to see if page returns an error. As well as check if property is an auction.
    if not is_url_valid(url_test):
        return False

    return True


def commit_updates_to_file() -> None:
    """Commits changes to file"""

    if urls:
        save_urls(urls, overwrite=to_overwrite, search=is_search, delete=to_delete)

    if is_search and not to_delete:
        print_captions(execute_s=True)
        time.sleep(DELAY_TO_GET_URLS)
        _get_urls_from_search()

    print_captions(execute=True)
    time.sleep(EXIT_TIMER)


def print_captions(mode=None, e=False, verifying_url=False, valid=True,
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
        print(f"\n{BAD}!!! Invalid URL... (Correct URL for Search/Property? Auction? [Not allowed]) !!!{END}")
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


def add_link(mode) -> None:
    """Logic for adding URLs"""

    global is_search

    print_captions(mode=mode)
    search_property_update = input()
    while search_property_update != search and search_property_update != property_ \
            and search_property_update != refresh and search_property_update != cancel:
        print_captions(mode=mode)
        search_property_update = input()

    if search_property_update != cancel:
        if search_property_update == search:
            print_captions(search_limitations=True)
            is_search = True
            _choose_options(a_o_d)
        elif search_property_update == property_:
            is_search = False
            _choose_options(a_o_d)
        elif search_property_update == refresh:
            is_search = True
            commit_updates_to_file()
    elif search_property_update == cancel:
        quit_program()
        return


def _choose_options(mode) -> None:
    """Handles the user choosing different options for URLs"""

    global to_overwrite, to_delete

    print_captions(mode=mode)
    append_overwrite_delete = input()
    while append_overwrite_delete != append and append_overwrite_delete != overwrite \
            and append_overwrite_delete != delete and append_overwrite_delete != cancel:
        print_captions(mode=mode)
        append_overwrite_delete = input()

    if append_overwrite_delete != cancel:
        if append_overwrite_delete == append:
            to_overwrite = False
            _get_urls_from_input(append)
        elif append_overwrite_delete == overwrite:
            to_overwrite = True
            _get_urls_from_input(overwrite)
        elif append_overwrite_delete == delete:
            to_delete = True
            _get_urls_from_input(delete)
    elif append_overwrite_delete == cancel:
        quit_program()
        return


def _get_urls_from_input(mode) -> None:
    """Gets URLs from user. Calls functions that adds them to file"""

    print_captions(mode=mode)
    new_url = get_url_from_input()

    if new_url != cancel:
        valid = url_is_valid(new_url)
        while not valid:
            print_captions(valid=False)

            print_captions(mode=mode)
            new_url = get_url_from_input()

            if new_url == cancel:
                quit_program()
                return

            valid = url_is_valid(new_url)

        urls.add(new_url)
        print_captions(received=True)

        print_captions(mode=mode, e=True)
        new_url = get_url_from_input()
        while new_url != cancel:

            if new_url == exe:
                commit_updates_to_file()
                return

            else:
                valid = url_is_valid(new_url)
                while not valid:
                    print_captions(valid=False)

                    print_captions(mode=mode, e=True)
                    new_url = get_url_from_input()

                    if new_url == exe:
                        commit_updates_to_file()
                        return

                    if new_url == cancel:
                        quit_program()
                        return

                    valid = url_is_valid(new_url)

                urls.add(new_url)
                print_captions(received=True)

            print_captions(mode=mode, e=True)
            new_url = get_url_from_input()

        if new_url == cancel:
            quit_program()
            return

    elif new_url == cancel:
        quit_program()
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
            urls_json['Search'][search_url] = list(set(get_all_urls_and_prices(search_url)))

        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump(urls_json, json_file, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump({'Search': {}, 'Property': {}}, json_file, indent=4)


if __name__ == '__main__':
    add_link(s_p_r)
