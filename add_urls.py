import time
import json
from user import get_url_from_input
from colors_for_print import PrintColors


def quit_program() -> None:
    """Quits programing without saving an data"""

    print_captions(c=True)
    time.sleep(1)


def url_is_valid(url) -> bool:
    """Checks if URL is valid"""

    if url[:23] == 'https://www.zillow.com/' and len(url) >= 29:
        return True
    return False


def commit_updates_to_file() -> None:
    """Commits changes to file"""
    pass


def print_captions(s_or_p=False, a_or_o=False, a=False, o=False, e=False, c=False, valid=True, received=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    BAD, OK, GOOD, GREAT = PrintColors.FAIL, PrintColors.WARNING, PrintColors.OKCYAN, PrintColors.OKGREEN
    END = PrintColors.ENDC

    if s_or_p:
        print(f"{GOOD}Do you want to update search URLs 's' or property URLs 'p'? ('c' to cancel):{END}", end=" ")
    elif a_or_o:
        print(f"{GOOD}Do you want to append 'a' or overwrite 'o'? ('c' to cancel):{END}", end=" ")
    elif a:
        print(f"{OK}--- Appending... URLs in this session will be saved to file! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}- Enter URL ('c' to cancel):{END}", end=" ")
    elif o:
        print(f"{OK}--- Overwriting... URLs before this session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL ('c' to cancel):{END}", end=" ")
    elif c:
        print(f"{BAD}!!! Ending program... No changes were made! !!!{END}")

    elif not valid:
        print(f"{BAD}!!! Invalid URL... Try again! !!!{END}")
    elif received:
        print(f"{GREAT}!!! URL received! !!!{END}")


def add_link() -> None:
    """Logic for adding URLs"""

    print_captions(s_or_p=True)
    search_or_property = input()
    while search_or_property != 's' and search_or_property != 'p' and search_or_property != 'c':
        print_captions(s_or_p=True)
        search_or_property = input()

    if search_or_property != 'c':

        if search_or_property == 's':

            print_captions(a_or_o=True)
            append_or_overwrite = input()
            while append_or_overwrite != 'a' and append_or_overwrite != 'o' and append_or_overwrite != 'c':
                print_captions(a_or_o=True)
                append_or_overwrite = input()

            if append_or_overwrite != 'c':

                if append_or_overwrite == 'a':
                    print('test')

                elif append_or_overwrite == 'o':
                    print_captions(o=True)
                    new_url = get_url_from_input()

                    if new_url != 'c':
                        valid = url_is_valid(new_url)
                        while not valid:
                            print_captions(valid=False)

                            print_captions(o=True)
                            new_url = get_url_from_input()

                            if new_url == 'c':
                                quit_program()
                                return

                            valid = url_is_valid(new_url)

                        print_captions(received=True)

                        print_captions(o=True, e=True)
                        new_url = get_url_from_input()
                        while new_url != 'c':

                            if new_url == 'e':
                                commit_updates_to_file()
                                return

                            else:
                                valid = url_is_valid(new_url)
                                while not valid:
                                    print_captions(valid=False)

                                    print_captions(o=True, e=True)
                                    new_url = get_url_from_input()

                                    if new_url == 'e':
                                        commit_updates_to_file()
                                        return

                                    if new_url == 'c':
                                        quit_program()
                                        return

                                    valid = url_is_valid(new_url)

                                print_captions(received=True)

                            print_captions(o=True, e=True)
                            new_url = get_url_from_input()

                        if new_url == 'c':
                            quit_program()
                            return

                    elif new_url == 'c':
                        quit_program()
                        return

            elif append_or_overwrite == 'c':
                quit_program()
                return

        elif search_or_property == 'p':
            print('test')

    elif search_or_property == 'c':
        quit_program()
        return

# try:
#     with open('urls.json', 'r') as json_file:
#         URLs = json.load(json_file)
#         URLs = {'Searches': [stuff], 'Properties': [stuff]}
#
#     if property_analysis[key]["Property Info"]["Price ($)"] != temp[key]["Property Info"]["Price ($)"]:
#         temp.update(property_analysis)
#         with open('urls.json', 'w') as json_file:
#             json.dump(temp, json_file, indent=4)
# except FileNotFoundError:
#     with open('urls.json', 'x') as json_file:
#         json.dump(property_analysis, json_file, indent=4)


add_link()
