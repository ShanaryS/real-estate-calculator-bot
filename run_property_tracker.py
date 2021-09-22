"""Use before run_analysis.py to choose urls. Can add property urls or search urls."""


import os.path
import json
import time
from data.calculations import save_urls
from data.user import get_url_from_input
from data.colors_for_print import PrintColors
from webscrapers.get_property_urls_from_search import is_url_valid, get_all_urls_and_prices


# Stores the urls from inputs. Gets written to file after add_link() is completed. If was cancelled, it gets cleared.
urls = set()

# Variables that dictate how each option that the user chooses is handled
to_overwrite = is_search = to_delete = False
s_p, search, property_, a_o_d = 's_p', 's', 'p', 'a_o_d'
append, overwrite, delete, cancel, exe = 'a', 'o', 'd', 'c', 'e'

# Used for delaying terminating program so user can read final text
SLEEP_TIMER = 1


def quit_program() -> None:
    """Quits programing without saving an data"""

    global to_overwrite, is_search, to_delete
    to_overwrite = is_search = to_delete = False
    urls.clear()

    print_captions(mode=cancel)
    time.sleep(SLEEP_TIMER)


def url_is_valid(url_test) -> bool:
    """Checks if URL is valid"""

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
    # Any search URL that has less than 400 listings (a hard requirement),
    # will have enough characters to never be affected by this.
    if len(url_test) < 100 and is_search:
        return False

    # Sends a get request to see if page returns an error. As well as check if property is an auction.
    if not is_url_valid(url_test):
        return False

    # If a property URL, return depending on mode user picked.
    if url_test[:27] == 'https://www.zillow.com/home' and len(url_test) >= 35:
        return True
    else:
        return False


def commit_updates_to_file() -> None:
    """Commits changes to file"""

    if urls:
        save_urls(urls, overwrite=to_overwrite, search=is_search, delete=to_delete)

    print_captions(execute=True)
    time.sleep(SLEEP_TIMER)


def print_captions(mode=None, e=False, verifying_url=False, valid=True,
                   received=False, execute=False, search_limitations=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    BAD, OK, GOOD, GREAT = PrintColors.FAIL, PrintColors.WARNING, PrintColors.OKCYAN, PrintColors.OKGREEN
    END = PrintColors.ENDC

    if mode == 's_p':
        print(f"{GOOD}Do you want to update search URLs 's' or property URLs 'p'? ('c' to cancel):{END}", end=" ")
    elif mode == 'a_o_d':
        print(f"{GOOD}Do you want to append 'a', overwrite 'o', or delete 'd'? ('c' to cancel):{END}", end=" ")
    elif mode == 'a':
        print(f"\n{OK}--- APPEND MODE... URLs in this session will be appended to file! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to append ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}- Enter URL to append ('c' to cancel):{END}", end=" ")
    elif mode == 'o':
        print(f"\n{OK}--- OVERWRITE MODE... URLs before this session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to write ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to write ('c' to cancel):{END}", end=" ")
    elif mode == 'd':
        print(f"\n{OK}--- DELETE MODE... URLs in session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to delete ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to delete ('c' to cancel):{END}", end=" ")
    elif mode == 'c':
        print(f"\n{BAD}!!! No changes were made! Ending program... !!!{END}")

    elif verifying_url:
        print(f"\n{OK}... Verifying URL ...{END}")
    elif not valid:
        print(f"\n{BAD}!!! Invalid URL... (Correct URL for Search/Property? Auction? [Not allowed]) !!!{END}")
    elif received:
        print(f"\n{GREAT}!!! URL received! !!!{END}")
    elif execute:
        print(f"\n{GREAT}!!! Committed changes to file! Ending program... !!!{END}")
    elif search_limitations:
        print(f"\n\n{BAD}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
              f"Zillow only displays 400 properties per search. If listings is above 400, certain properties\n"
              f"CANNOT be accessed. Instead, filter number of listings heavily to make sure it does not\n"
              f"exceed 400. Split the search criteria into multiple separate searches.\n\n"
              
              f"{OK}For example: Instead of a single URL with a price range of $100k-$1M, use two URLs with price\n"
              f"ranges of $100k-$500k and $500k-$1M. Assuming each of those searches return less than 400 listings.\n"
              f"P.S 'Agent' listing URLs doesn't include 'Other' properties. Add both URLs to include all properties.\n"
              f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{END}\n")


def add_link(mode) -> None:
    """Logic for adding URLs"""

    global is_search

    print_captions(mode=mode)
    search_or_property = input()
    while search_or_property != search and search_or_property != property_ and search_or_property != cancel:
        print_captions(mode=mode)
        search_or_property = input()

    if search_or_property != cancel:
        if search_or_property == search:
            print_captions(search_limitations=True)
            is_search = True
            _choose_options(a_o_d)
        elif search_or_property == property_:
            is_search = False
            _choose_options(a_o_d)
    elif search_or_property == cancel:
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


if __name__ == '__main__':
    add_link(s_p)

    try:
        with open(os.path.join('output', 'urls.json')) as json_file:
            urls_json = json.load(json_file)

        for url in urls_json.setdefault('Search', dict()):
            urls_json.update(get_all_urls_and_prices(url))

        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump(urls_json, json_file, indent=4)

    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        with open(os.path.join('output', 'urls.json'), 'w') as json_file:
            json.dump({'Search': {}, 'Property': {}}, json_file, indent=4)
