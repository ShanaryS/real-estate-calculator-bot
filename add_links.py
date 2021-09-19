import json
from get_property_info import set_url_property


to_update = input("Do you want to update search links 's' or property links 'p'? ('c' to cancel): ")
while to_update != 's' and to_update != 'p' and to_update != 'c':
    to_update = input("Do you want to update search links 's' or property links 'p'? ('c' to cancel): ")

if to_update != 'c':
    if to_update == 's':
        append_overwrite = input("Do you want to append 'a' or overwrite 'o'? ('c' to cancel): ")
        while append_overwrite != 'a' and append_overwrite != 'o' and append_overwrite != 'c':
            append_overwrite = input("Do you want to append 'a' or overwrite 'o'? ('c' to cancel): ")

        if append_overwrite != 'c':
            if append_overwrite == 'a':
                try:
                    with open('links.json', 'r') as json_file:
                        links = json.load(json_file)
                        links = {'Searches': [stuff], 'Properties': [stuff]}

                    if property_analysis[key]["Property Info"]["Price ($)"] != temp[key]["Property Info"]["Price ($)"]:
                        temp.update(property_analysis)
                        with open('links.json', 'w') as json_file:
                            json.dump(temp, json_file, indent=4)
                except FileNotFoundError:
                    with open('links.json', 'x') as json_file:
                    json.dump(property_analysis, json_file, indent=4)

            elif append_overwrite == 'o':
                print("Overwriting... Links before this session will be lost!")
                new_link = input("Enter link ('c' to cancel): ")
                if new_link != 'c':
                    send link to program, perfrom some check to see if valid
                    while not sucessful:
                        print(">>> Invalid url. Try again\n")

                        print("Overwriting... Links before this session will be lost!")
                        new_link = input("Enter link ('c' to cancel): ")
                        send link to program, perfrom some check to see if valid

                    print(">>> Link received\n")

                    print("Overwriting... Links before this session will be lost!")
                    new_link = input("Enter another link ('e' to execute changes, 'c' to cancel): ")
                    while new_link != 'c':
                        if new_link == 'e':
                            commit changes to file
                        else:
                            send link to program, perfrom some check to see if valid
                            while not sucessful:
                                print(">>> Invalid url. Try again\n")

                                print("Overwriting... Links before this session will be lost!")
                                new_link = input("Enter link ('c' to cancel): ")
                                send link to program, perfrom some check to see if valid

                            print(">>> Link received\n")

                            print("Overwriting... Links before this session will be lost!")
                            new_link = input("Enter another link ('e' to execute changes, 'c' to cancel): ")


    elif to_update == 'p':
