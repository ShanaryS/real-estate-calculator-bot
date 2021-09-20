"""Main script to run. Saves analysis to file based on urls.json. Add to urls.json by running run_urls_update.py.
For search urls, the URLs for the houses are found at run time and then added urls.json inside 'Property' object. This
is the same place where adding a single property would also be stored. Then program gets the info for all houses in
the 'Property' object.
"""


from data.calculations import update_values, get_property_analysis, write_property_analyses, is_new_analyses
from data.colors_for_print import PrintColors
import json
import time


TIME_BETWEEN_REQUESTS = 1
keys = []
property_analyses = []


try:
    with open('urls.json', 'r') as json_file:
        urls_json = json.load(json_file)

    print(f"\n{PrintColors.OKCYAN}Getting URLs from saved searches...{PrintColors.ENDC}\n")

    '''
    for url in urls_json['Search']:
        # Add urls to urls.json under property, save_urls
        time.sleep(TIME_BETWEEN_REQUESTS)
    '''

    # Update analysis.json if URLs were deleted
    try:
        with open('analysis.json', 'r') as json_file:
            analysis_json = json.load(json_file)

        temp = []
        for i in analysis_json:
            if analysis_json[i]["Property URL"] not in urls_json["Property"]:
                temp.append(i)
        for i in temp:
            analysis_json.pop(i)

        with open('analysis.json', 'w') as json_file:
            json.dump(analysis_json, json_file, indent=4)

    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, TypeError):
        with open('analysis.json', 'w') as json_file:
            json.dump({}, json_file, indent=4)

    print(f"{PrintColors.WARNING}Analyzing houses... "
          f"Expected duration: {int(len(urls_json['Property']) * (1.5 + TIME_BETWEEN_REQUESTS))}s{PrintColors.ENDC}\n")

    update_interest_rate = True
    for url in urls_json['Property']:
        print(url)
        update_values(url=url, save_to_file=False, update_interest_rate=update_interest_rate)
        key, property_analysis = get_property_analysis()
        keys.append(key)
        property_analyses.append(property_analysis)
        update_interest_rate = False
        time.sleep(TIME_BETWEEN_REQUESTS)

    write_property_analyses(keys, property_analyses)

    if not all(is_new_analyses()):
        print(f"\n{PrintColors.FAIL}No new analysis to add...{PrintColors.ENDC}")

except FileNotFoundError:
    print("Error: No URLs added.")


'''
If not printing url:
To troubleshoot problematic links, use urls.json. You CANNOT just look at the last analysis saved as the saved order
is random. Something like searching the amount of times that address shows up in analysis.json should give the
index of the problematic url in urls.json['Property']. The houses are done in order of that file. Note though, whenever 
a url is added to the file, the order changes. This doesn't matter in this case since properties are only searched 
after all the urls are added.

For troubleshooting adding urls automatically from 'Search', it should be so few that you can manually check.
'''
