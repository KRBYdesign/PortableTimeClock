import os
import requests
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

IP = "192.168.10.102"
PORT = 5000

def clear():
    os.system('cls' if os.name == "nt" else "clear")

def getAllUsers():
    print(f"{bcolors.OKCYAN}Fetching all users...{bcolors.ENDC}")
    res = requests.get(f"http://{IP}:{PORT}/manage/all-users")
    parsedRequest = json.loads(res.text)

    return parsedRequest['payload']

def getAllDuplicateIds(all_records):
    print(f"{bcolors.OKCYAN}Checking for duplicates IDs...{bcolors.ENDC}")
    ids_list = []
    dupe_list = []

    for record in all_records:
        if record['number'] not in ids_list:
            ids_list.append(record['number'])
        else:
            dupe_list.append(record['number'])

    if len(dupe_list) > 0:
        print(f"{bcolors.WARNING}Duplicate IDs found{bcolors.ENDC}")

    return dupe_list

def getAllDuplicateNames(all_records):
    print(f"{bcolors.OKCYAN}Checking for duplicate names...{bcolors.ENDC}")
    names_list = []
    dupe_list = []

    for record in all_records:
        if record['name'] not in names_list:
            names_list.append(record['name'])
        else:
            dupe_list.append(record['name'])

    if len(dupe_list) > 0:
        print(f"{bcolors.WARNING}Duplicate names found{bcolors.ENDC}")
    
    return dupe_list

if __name__ == "__main__":
    clear()
    print(f"{bcolors.HEADER}Establishing connection...{bcolors.ENDC}")

    try:
        result = requests.get(f"http://{IP}:{PORT}/manage")
        print(f"{bcolors.OKGREEN}Connection Established{bcolors.ENDC}")
    except requests.exceptions.RequestException as err:
        print(f"{bcolors.WARNING}Server is not responding. Ensure server is active.\n\n{bcolors.FAIL}ERROR: {err}\n\n{bcolors.WARNING}Exiting...{bcolors.ENDC}")
        quit(2)
    except:
        print(f"{bcolors.FAIL}Something went wrong establishing connection to the server.{bcolors.ENDC}")
        quit(2)

    all_records = getAllUsers()
    
    duplicate_ids = getAllDuplicateIds(all_records)

    duplicate_names = getAllDuplicateNames(all_records)

    if len(duplicate_ids) == 0 and len(duplicate_names) == 0:
        print(f"{bcolors.OKGREEN}Done. No duplicates found.{bcolors.ENDC}")
        quit()

    else:
        if len(duplicate_ids) > 0:
            print(f"{bcolors.WARNING}Duplicate IDs:{bcolors.ENDC}")

            for index, id in enumerate(duplicate_ids):
                print(f"    {index + 1}: {id}")
            
            print(f"{bcolors.BOLD}Total Duplicate IDs: {len(duplicate_ids)}")
            print()

        elif len(duplicate_names) > 0:
            print(f"{bcolors.WARNING}Duplicate Names:{bcolors.ENDC}")

            for index, name in enumerate(duplicate_names):
                print(f"    {index + 1}: {name}")
            
            print(f"{bcolors.BOLD}Total Duplicate IDs: {len(duplicate_names)}")
            print()

        quit()
