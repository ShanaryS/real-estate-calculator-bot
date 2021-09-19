import time
import json
from colors_for_print import PrintColors


def quit_program() -> None:
    """Quits programing without saving an data"""

    print_captions(c=True)
    time.sleep(1.5)


def url_is_valid(url) -> bool:
    """Checks if url is valid"""

    if url[:23] == 'https://www.zillow.com/' and len(url) >= 29:
        return True
    return False


def commit_updates_to_file() -> None:
    """Commits changes to file"""
    pass


def print_captions(s_or_p=False, a_or_o=False, a=False, o=False, e=False, c=False, valid=True, received=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    if s_or_p:
        print("Do you want to update search urls 's' or property urls 'p'? ('c' to cancel):", end=" ")
    elif a_or_o:
        print("Do you want to append 'a' or overwrite 'o'? ('c' to cancel):", end=" ")
    elif a:
        print("--- Appending... Urls in this session will be saved to file! ---")
        if e:
            print("Enter another url ('e' to execute changes, 'c' to cancel):", end=" ")
        else:
            print("- Enter url ('c' to cancel):", end=" ")
    elif o:
        print("--- Overwriting... Urls before this session will be lost! ---")
        if e:
            print("Enter another url ('e' to execute changes, 'c' to cancel):", end=" ")
        else:
            print("Enter url ('c' to cancel):", end=" ")
    elif c:
        print("!!! Ending program... No changes were made !!!")

    elif not valid:
        print("!!! Invalid url. Try again !!!")
    elif received:
        print("!!! Link received !!!")


def add_link() -> None:
    """Logic for adding urls"""

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
                    new_url = input()

                    if new_url != 'c':
                        valid = url_is_valid(new_url)
                        while not valid:
                            print_captions(valid=False)

                            print_captions(o=True)
                            new_url = input()

                            if new_url == 'c':
                                quit_program()
                                return

                            valid = url_is_valid(new_url)

                        print_captions(received=True)

                        print_captions(o=True, e=True)
                        new_url = input()
                        while new_url != 'c':

                            if new_url == 'e':
                                commit_updates_to_file()
                                return

                            else:
                                valid = url_is_valid(new_url)
                                while not valid:
                                    print_captions(valid=False)

                                    print_captions(o=True, e=True)
                                    new_url = input()

                                    if new_url == 'e':
                                        commit_updates_to_file()
                                        return

                                    if new_url == 'c':
                                        quit_program()
                                        return

                                    valid = url_is_valid(new_url)

                                print_captions(received=True)

                            print_captions(o=True, e=True)
                            new_url = input()

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
#         urls = json.load(json_file)
#         urls = {'Searches': [stuff], 'Properties': [stuff]}
#
#     if property_analysis[key]["Property Info"]["Price ($)"] != temp[key]["Property Info"]["Price ($)"]:
#         temp.update(property_analysis)
#         with open('urls.json', 'w') as json_file:
#             json.dump(temp, json_file, indent=4)
# except FileNotFoundError:
#     with open('urls.json', 'x') as json_file:
#         json.dump(property_analysis, json_file, indent=4)


add_link()
