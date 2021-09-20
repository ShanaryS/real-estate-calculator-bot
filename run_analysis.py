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

    for url in urls_json['Property']:
        update_values(url=url, save_to_file=True)
        time.sleep(TIME_BETWEEN_REQUESTS)

except FileNotFoundError:
    print("Error: No URLs added.")
