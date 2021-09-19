import time
import json


def quit_program() -> None:
    """Quits programing without saving an data"""

    print(">>> Ending program... No changes were made")
    time.sleep(1)


def url_is_valid(url) -> bool:
    """Checks if url is valid"""

    if url[:23] == 'https://www.zillow.com/' and len(url) >= 29:
        return True
    return False


def commit_updates_to_file() -> None:
    """Commits changes to file"""
    pass


def print_overwrite_caption(execute=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    print("Overwriting... urls before this session will be lost!")
    if execute:
        print("Enter another url ('e' to execute changes, 'c' to cancel):", end=" ")
    else:
        print("Enter url ('c' to cancel):", end=" ")


def print_append_caption(execute=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    print("Appending... urls in this session will be saved to file!")
    if execute:
        print("Enter another url ('e' to execute changes, 'c' to cancel):", end=" ")
    else:
        print("Enter url ('c' to cancel):", end=" ")


def add_link() -> None:
    """Logic for adding urls"""

    to_update = input("Do you want to update search urls 's' or property urls 'p'? ('c' to cancel): ")
    while to_update != 's' and to_update != 'p' and to_update != 'c':
        to_update = input("Do you want to update search urls 's' or property urls 'p'? ('c' to cancel): ")

    if to_update != 'c':

        if to_update == 's':
            append_overwrite = input("Do you want to append 'a' or overwrite 'o'? ('c' to cancel): ")
            while append_overwrite != 'a' and append_overwrite != 'o' and append_overwrite != 'c':
                append_overwrite = input("Do you want to append 'a' or overwrite 'o'? ('c' to cancel): ")

            if append_overwrite != 'c':

                if append_overwrite == 'a':
                    print('test')

                elif append_overwrite == 'o':
                    print_overwrite_caption()
                    new_url = input()

                    if new_url != 'c':
                        valid = url_is_valid(new_url)
                        while not valid:
                            print(">>> Invalid url. Try again\n")

                            print_overwrite_caption()
                            new_url = input()

                            if new_url == 'c':
                                quit_program()
                                return

                            valid = url_is_valid(new_url)

                        print(">>> Link received\n")

                        print_overwrite_caption(execute=True)
                        new_url = input()
                        while new_url != 'c':

                            if new_url == 'e':
                                commit_updates_to_file()
                                return

                            else:
                                valid = url_is_valid(new_url)
                                while not valid:
                                    print(">>> Invalid url. Try again\n")

                                    print_overwrite_caption(execute=True)
                                    new_url = input()

                                    if new_url == 'e':
                                        commit_updates_to_file()
                                        return

                                    if new_url == 'c':
                                        quit_program()
                                        return

                                    valid = url_is_valid(new_url)

                                print(">>> Link received\n")

                                print_overwrite_caption(execute=True)
                                new_url = input()

                    elif new_url == 'c':
                        quit_program()
                        return

            elif append_overwrite == 'c':
                quit_program()
                return

        elif to_update == 'p':
            pass

    elif to_update == 'c':
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
