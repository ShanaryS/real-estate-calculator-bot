from calculations import update_values
import json
import time


TIME_BETWEEN_REQUESTS = 1


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
        update_values(url=url, save_to_file=True, update_interest_rate=update_interest_rate)
        update_interest_rate = False
        time.sleep(TIME_BETWEEN_REQUESTS)

except FileNotFoundError:
    print("Error: No URLs added.")

'''
To troubleshoot problematic links, use urls.json. You CANNOT just look at the last analysis saved as the saved order
is random. Something like searching the amount of times that address shows up in analysis.json should give the
index of the problematic url in urls.json['Property']. The houses are done in order of that file. Note though, whenever 
a url is added to the file, the order changes. This doesn't matter in this case since properties are only searched 
after all the urls are added.

For troubleshooting adding urls automatically from 'Search', it should be so few that you can manually check.
'''
