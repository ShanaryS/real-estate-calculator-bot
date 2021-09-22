"""Main script to run. Saves analysis to file based on urls.json. Add to urls.json by running run_property_tracker.py.
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
from web.get_property_info import TIME_BETWEEN_REQUESTS
from run_property_tracker import SLEEP_TIMER


GET_REQUEST_EXPECTED_TIME = 1.75
keys = []
property_analyses = []
url_removed = False


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

    # Tell user how long analysis is expected to take
    num_property_urls = len(urls_json.setdefault('Property', dict()))
    num_search_urls = 0
    for search_url in urls_json.setdefault('Search', dict()):
        num_search_urls += len(urls_json['Search'][search_url])
    num_urls = num_search_urls + num_property_urls
    TIME_CONST = GET_REQUEST_EXPECTED_TIME + TIME_BETWEEN_REQUESTS
    expected_time = int(num_urls * TIME_CONST)
    print(f"{PrintColors.WARNING}--- Analyzing properties... Expected duration: {PrintColors.OKCYAN}"
          f"{expected_time}s{PrintColors.ENDC}\n")

    for index, url in enumerate(urls_json.setdefault('Property', dict())):
        print(f"{PrintColors.WARNING}TIME REMAINING: "
              f"{PrintColors.OKCYAN}{-int(-(expected_time - index * TIME_CONST))}s{PrintColors.ENDC}",
              "---", url)
        update_values(url=url, save_to_file=False, update_interest_rate=False)
        key, property_analysis = get_property_analysis()
        keys.append(key)
        property_analyses.append(property_analysis)
        time.sleep(TIME_BETWEEN_REQUESTS)
    write_property_analyses(keys, property_analyses)

    # If above changed the file, save that fact to print closing text.
    if any(is_new_analyses()) or url_removed:
        updated = True
    else:
        updated = False

    # Could just call write_property_analyses() once after loops, but want to separate these to act like a save point.
    keys.clear(), property_analyses.clear()
    for search_url in urls_json.setdefault('Search', dict()):
        for index, url in enumerate(urls_json['Search'][search_url]):
            print(f"{PrintColors.WARNING}TIME REMAINING: "
                  f"{PrintColors.OKCYAN}{-int(-(expected_time - index * TIME_CONST))}s{PrintColors.ENDC}",
                  "---", url)
            update_values(url=url, save_to_file=False, update_interest_rate=False)
            key, property_analysis = get_property_analysis()
            keys.append(key)
            property_analyses.append(property_analysis)
            time.sleep(TIME_BETWEEN_REQUESTS)
    write_property_analyses(keys, property_analyses)

    if updated:
        check_if_analysis_json_updated(check=True)


def check_if_analysis_json_updated(check=False) -> None:
    """Checks if the analysis performed yielded any new results"""

    if any(is_new_analyses()) or url_removed or check:
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

        sync_urls_and_analysis_data()
        get_interest_rate()
        analyze_properties()

    except FileNotFoundError:
        print(f"\n{PrintColors.FAIL}!!! Error: No URLs exist... !!!{PrintColors.ENDC}")
        print(f"{PrintColors.OKGREEN}Run run_property_tracker.py first.{PrintColors.ENDC}")
        time.sleep(3)
