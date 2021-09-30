"""Main script to run. Saves analysis to file based on urls.json.
Add to urls.json by running run_property_tracker.py.
For search urls, the URLs for the houses are found at run time and
then added urls.json inside 'Property' object. This
is the same place where adding a single property would also be stored.
Then program gets the info for all houses in the 'Property' object.
"""

import os.path
from dataclasses import dataclass
import json
import time
from data.calculations import update_values, get_property_analysis, \
    write_property_analyses, is_new_analyses
from web.push_best_deals_to_email import email_best_deals
from data.user import set_interest_rate
from data.colors_for_print import BAD, OK, GOOD, GREAT, END
from web.get_property_info import TIME_BETWEEN_REQUESTS
from run_property_tracker import EXIT_TIMER

GET_REQUEST_EXPECTED_TIME = 1.5


@dataclass
class State:
    """Stores the state of the analysis"""

    keys: list
    property_analyses: list
    url_removed: bool


def _get_interest_rate() -> None:
    """Gets current interest rate to use for analyses in current session"""
    set_interest_rate()


def _analyze_property(state, url) -> None:
    """Analyze a single property"""

    # If statement ignores property if there was an error getting the data.
    if update_values(url=url, save_to_file=False, update_interest_rate=False):
        print()  # Moves to next line
        key, property_analysis = get_property_analysis()
        state.keys.append(key)
        state.property_analyses.append(property_analysis)
    else:
        print(f" {BAD}!!! ERROR ANALYZING THIS PROPERTY. "
              f"CHECK \\output\\errors.log FOR DETAILS. !!!{END}")

    time.sleep(TIME_BETWEEN_REQUESTS)


def _analyze_properties(state, urls_json) -> None:
    """Gets info for all properties and saves them to analysis.json"""

    # Tell user how long analysis is expected to take
    num_property_urls = len(urls_json.setdefault('Property', dict()))
    num_search_urls = 0
    for search_url in urls_json.setdefault('Search', dict()):
        num_search_urls += len(urls_json['Search'][search_url])
    num_urls = num_search_urls + num_property_urls
    TIME_CONST = GET_REQUEST_EXPECTED_TIME + TIME_BETWEEN_REQUESTS
    expected_time = int(num_urls * TIME_CONST)
    index = 0
    print(f"{OK}--- Analyzing properties... Expected duration: {GOOD}"
          f"{expected_time}s{END}\n")

    # Gets analysis and writes to file for the individually added properties
    for url in urls_json.setdefault('Property', dict()):
        print(f"{OK}TIME REMAINING: "
              f"{GOOD}{-int(-(expected_time - index * TIME_CONST))}s{END}",
              "---", url, end="")
        _analyze_property(state, url)
        index += 1
    write_property_analyses(state.keys, state.property_analyses)

    # If above changed the file, save that fact to print closing text.
    if any(is_new_analyses()) or state.url_removed:
        updated = True
    else:
        updated = False

    # Could just call write_property_analyses() once after loops,
    # but want to separate these to act like a save point.
    state.keys.clear(), state.property_analyses.clear()
    for search_url in urls_json.setdefault('Search', dict()):
        for url in urls_json['Search'][search_url]:
            print(f"{OK}TIME REMAINING: "
                  f"{GOOD}{-int(-(expected_time - index * TIME_CONST))}s{END}",
                  "---", url, end="")
            _analyze_property(state, url)
            index += 1
    write_property_analyses(state.keys, state.property_analyses)

    if updated:
        _check_if_analysis_json_updated(state, check=True)


def _check_if_analysis_json_updated(state, check=False) -> None:
    """Checks if the analysis performed yielded any new results"""

    if any(is_new_analyses()) or state.url_removed or check:
        print(f"\n{GREAT}"
              f"!!! Analyses were successfully added/updated! !!!{END}")
    else:
        print(f"\n{BAD}!!! No new analysis to add/update! !!!{END}")
    time.sleep(EXIT_TIMER)  # Delays closing the program so user can read text


def main() -> None:
    """Main function"""

    state = State(
        keys=[],
        property_analyses=[],
        url_removed=False
    )

    try:
        with open(os.path.join('output', 'urls.json')) as json_file:
            urls_json = json.load(json_file)

        _get_interest_rate()
        _analyze_properties(state, urls_json)
        email_best_deals()

    except FileNotFoundError:
        print(f"\n{BAD}!!! Error: No URLs exist... !!!{END}")
        print(f"{GREAT}Run run_property_tracker.py first.{END}")
        time.sleep(3)


if __name__ == '__main__':
    main()
