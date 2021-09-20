"""Main script to run. Saves analysis to file based on urls.json. Add to urls.json by running run_urls_update.py.
For search urls, the URLs for the houses are found at run time and then added urls.json inside 'Property' object. This
is the same place where adding a single property would also be stored. Then program gets the info for all houses in
the 'Property' object.
"""


import os.path
import json
import time
from data.calculations import update_values, get_property_analysis, write_property_analyses, is_new_analyses
from data.user import set_interest_rate
from data.colors_for_print import PrintColors
from webscrapers.get_property_info import TIME_BETWEEN_REQUESTS
from run_urls_update import SLEEP_TIMER


keys = []
property_analyses = []
url_removed = False


def add_urls_to_property_from_search() -> None:
    """Calls web scraper for search urls then????????"""

    print(f"\n{PrintColors.WARNING}--- Getting URLs from saved searches...{PrintColors.ENDC}\n")

    '''
    for url in urls_json['Search']:
        # Add urls to urls.json under property, save_urls
        time.sleep(TIME_BETWEEN_REQUESTS)
    '''


def sync_urls_and_analysis_data() -> None:
    """Updates analysis.json if URLs were deleted"""

    print(f"{PrintColors.WARNING}--- Removing any analysis not tracked in urls.json...{PrintColors.ENDC}\n")

    # Update analysis.json if URLs were deleted
    try:
        with open(os.path.join('output', 'analysis.json')) as file:
            analysis_json = json.load(file)

        # Think this can be simplified using set().intersection_update()
        temp = []
        for i in analysis_json:
            if analysis_json[i]["Property URL"] not in urls_json["Property"]:
                temp.append(i)
        for i in temp:
            analysis_json.pop(i)

        if temp:
            global url_removed
            url_removed = True
            with open(os.path.join('output', 'analysis.json'), 'w') as file:
                json.dump(analysis_json, file, indent=4)

    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, TypeError):
        with open(os.path.join('output', 'analysis.json'), 'w') as file:
            json.dump({}, file, indent=4)


def get_interest_rate() -> None:
    """Gets current interest rate to use for analyses in current session"""

    print(f"{PrintColors.WARNING}--- Getting current interest rates...{PrintColors.ENDC}\n")
    set_interest_rate()


def analyze_properties() -> None:
    """Gets info for all properties and saves them to analysis.json"""

    num_urls = len(urls_json['Property'])
    print(f"{PrintColors.WARNING}--- Analyzing properties... Expected duration: "
          f"{PrintColors.OKGREEN}{int(num_urls * (1.75 + TIME_BETWEEN_REQUESTS))}s{PrintColors.ENDC}\n")

    for url in urls_json['Property']:
        print(url)
        update_values(url=url, save_to_file=False, update_interest_rate=False)
        key, property_analysis = get_property_analysis()
        keys.append(key)
        property_analyses.append(property_analysis)
        time.sleep(TIME_BETWEEN_REQUESTS)

    write_property_analyses(keys, property_analyses)


def check_if_analysis_json_updated() -> None:
    """Checks if the analysis performed yielded any new results"""

    if any(is_new_analyses()) or url_removed:
        print(f"\n{PrintColors.OKGREEN}"
              f"!!! Analyses were successfully added/updated! Ending program... !!!{PrintColors.ENDC}")
    else:
        print(f"\n{PrintColors.FAIL}!!! No new analysis to add/update! Ending program... !!!{PrintColors.ENDC}")
    time.sleep(SLEEP_TIMER)  # Delays closing the program so user can read final text


# Calls all the above functions to perform the analysis
if __name__ == '__main__':
    try:
        with open(os.path.join('output', 'urls.json')) as json_file:
            urls_json = json.load(json_file)

        add_urls_to_property_from_search()
        sync_urls_and_analysis_data()
        get_interest_rate()
        analyze_properties()
        check_if_analysis_json_updated()

    except FileNotFoundError:
        print(f"\n{PrintColors.FAIL}!!! Error: No URLs exist... !!!{PrintColors.ENDC}")
        print(f"{PrintColors.OKGREEN}Run run_urls_update.py first.{PrintColors.ENDC}")
        time.sleep(3)
