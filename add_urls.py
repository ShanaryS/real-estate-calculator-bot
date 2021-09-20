import time
from calculations import save_urls
from user import get_url_from_input
from colors_for_print import PrintColors


# Stores the urls from inputs. Gets written to file after add_link() is completed. If was cancelled, it gets cleared.
urls = set()
overwrite = search = delete = False
sleep_timer = 1


def quit_program() -> None:
    """Quits programing without saving an data"""

    global overwrite, search
    overwrite = search = False
    urls.clear()

    print_captions(c=True)
    time.sleep(sleep_timer)


def url_is_valid(url) -> bool:
    """Checks if URL is valid"""

    if url[:23] == 'https://www.zillow.com/' and len(url) >= 29:
        return True
    return False


def commit_updates_to_file() -> None:
    """Commits changes to file"""

    if urls:
        save_urls(urls, overwrite=overwrite, search=search, delete=delete)

    print_captions(execute=True)
    time.sleep(sleep_timer)


def print_captions(s_p=False, a_o_d=False, a=False, o=False, d=False, e=False,
                   c=False, valid=True, received=False, execute=False) -> None:
    """Prints text that tells the user what the programing is doing"""

    BAD, OK, GOOD, GREAT = PrintColors.FAIL, PrintColors.WARNING, PrintColors.OKCYAN, PrintColors.OKGREEN
    END = PrintColors.ENDC

    if s_p:
        print(f"{GOOD}Do you want to update search URLs 's' or property URLs 'p'? ('c' to cancel):{END}", end=" ")
    elif a_o_d:
        print(f"{GOOD}Do you want to append 'a', overwrite 'o', or delete 'd'? ('c' to cancel):{END}", end=" ")
    elif a:
        print(f"{OK}--- Appending... URLs in this session will be appended to file! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to append ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}- Enter URL to append ('c' to cancel):{END}", end=" ")
    elif o:
        print(f"{OK}--- Overwriting... URLs before this session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to write ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to write ('c' to cancel):{END}", end=" ")
    elif d:
        print(f"{OK}--- Deleting... URLs in session will be lost! ---{END}")
        if e:
            print(f"{GOOD}Enter another URL to delete ('e' to execute changes, 'c' to cancel):{END}", end=" ")
        else:
            print(f"{GOOD}Enter URL to delete ('c' to cancel):{END}", end=" ")
    elif c:
        print(f"{BAD}!!! Ending program... No changes were made! !!!{END}")

    elif not valid:
        print(f"{BAD}!!! Invalid URL... Try again! !!!{END}")
    elif received:
        print(f"{GREAT}!!! URL received! !!!{END}")
    elif execute:
        print(f"{GREAT}!!! Committed changes to file! !!!{END}")


def add_link() -> None:
    """Logic for adding URLs"""

    print_captions(s_p=True)
    search_or_property = input()
    while search_or_property != 's' and search_or_property != 'p' and search_or_property != 'c':
        print_captions(s_p=True)
        search_or_property = input()

    if search_or_property != 'c':

        if search_or_property == 's':
            global search
            search = True

            print_captions(a_o_d=True)
            append_overwrite_delete = input()
            while append_overwrite_delete != 'a' and append_overwrite_delete != 'o'\
                    and append_overwrite_delete != 'd' and append_overwrite_delete != 'c':
                print_captions(a_o_d=True)
                append_overwrite_delete = input()

            if append_overwrite_delete != 'c':

                if append_overwrite_delete == 'a':
                    print('test')

                elif append_overwrite_delete == 'o':
                    global overwrite
                    overwrite = True

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

                        urls.add(new_url)
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

                                urls.add(new_url)
                                print_captions(received=True)

                            print_captions(o=True, e=True)
                            new_url = get_url_from_input()

                        if new_url == 'c':
                            quit_program()
                            return

                    elif new_url == 'c':
                        quit_program()
                        return

                elif append_overwrite_delete == 'd':
                    global delete
                    delete = True

                    print_captions(d=True)
                    new_url = get_url_from_input()

                    if new_url != 'c':
                        valid = url_is_valid(new_url)
                        while not valid:
                            print_captions(valid=False)

                            print_captions(d=True)
                            new_url = get_url_from_input()

                            if new_url == 'c':
                                quit_program()
                                return

                            valid = url_is_valid(new_url)

                        urls.add(new_url)
                        print_captions(received=True)

                        print_captions(d=True, e=True)
                        new_url = get_url_from_input()
                        while new_url != 'c':

                            if new_url == 'e':
                                commit_updates_to_file()
                                return

                            else:
                                valid = url_is_valid(new_url)
                                while not valid:
                                    print_captions(valid=False)

                                    print_captions(d=True, e=True)
                                    new_url = get_url_from_input()

                                    if new_url == 'e':
                                        commit_updates_to_file()
                                        return

                                    if new_url == 'c':
                                        quit_program()
                                        return

                                    valid = url_is_valid(new_url)

                                urls.add(new_url)
                                print_captions(received=True)

                            print_captions(d=True, e=True)
                            new_url = get_url_from_input()

                        if new_url == 'c':
                            quit_program()
                            return

                    elif new_url == 'c':
                        quit_program()
                        return

            elif append_overwrite_delete == 'c':
                quit_program()
                return

        elif search_or_property == 'p':
            print('test')

    elif search_or_property == 'c':
        quit_program()
        return


add_link()
