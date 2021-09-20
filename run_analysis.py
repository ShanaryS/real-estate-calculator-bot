"""Main script to run. Saves analysis to file based on urls.json. Add to urls.json by running add_urls.py.
For search urls, the URLs for the houses are found at run time and then added urls.json inside 'Property' object. This
is the same place where adding a single property would also be stored. Then program gets the info for all houses in
the 'Property' object.
"""


from calculations import update_values, is_new_analysis
from colors_for_print import PrintColors
import json
import time


TIME_BETWEEN_REQUESTS = 1
new_analysis_list = []


try:
    with open('urls.json', 'r') as json_file:
        urls_json = json.load(json_file)

    '''
    for url in urls_json['Search']:
        # Add urls to urls.json under property
        time.sleep(TIME_BETWEEN_REQUESTS)
    '''

    update_interest_rate = True
    for url in urls_json['Property']:
        print(url)
        update_values(url=url, save_to_file=True, update_interest_rate=update_interest_rate)
        new_analysis_list.append(is_new_analysis())
        update_interest_rate = False
        time.sleep(TIME_BETWEEN_REQUESTS)

    if not all(new_analysis_list):
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
