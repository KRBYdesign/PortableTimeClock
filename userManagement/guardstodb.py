import os
import csv
import requests
import json

#TODO Make mock data to test appending of multiple rounds of users to database with recursive checking on ID numbers.

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

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def registerUser(name, id):
    url = 'http://192.168.10.102:5000/register/python'
    myobj = {
        "name": name,
        "id": id,
    }

    req = requests.post(url, json=myobj)
    print(f"{bcolors.OKGREEN}{req.text}{bcolors.ENDC}")

def chooseCorrectCsvFile(file_list):
    print(f"{bcolors.WARNING}Multiple valid CSV files found. Please choose the correct one.{bcolors.ENDC}")
    print()

    for index, file in enumerate(file_list):
        print(f"  {bcolors.OKBLUE}{index}{bcolors.ENDC} -> {file}")

    user_choice = int(input(f"{bcolors.WARNING}Selection: "))
    print(bcolors.ENDC)

    try:
        return file_list[user_choice]
    except IndexError:
        clear()
        print(f"{bcolors.FAIL}Invalid file choice. Please choose a valid file.{bcolors.ENDC}")
        correct_file = chooseCorrectCsvFile(file_list)
        return correct_file
    except TypeError:
        clear()
        print(f"{bcolors.FAIL}Invalid option. Please use numbers only.{bcolors.ENDC}")
        correct_file = chooseCorrectCsvFile(file_list)
        return correct_file

def getCSV():
    current_dir = os.getcwd()
    all_files = os.listdir(current_dir)
    csv_files = []

    for file in all_files:
        if file.endswith(".csv") and file.startswith("Confirmed"):
            csv_files.append(file)

    if len(csv_files) == 0:
        print(f"{bcolors.FAIL}No CSV files were located in {current_dir}. Exiting{bcolors.ENDC}")
        quit()
    elif len(csv_files) == 1:
        return csv_files[0]
    elif len(csv_files) > 1:
        correct_file = chooseCorrectCsvFile(csv_files)
        return correct_file

def bulkAddToDb(user_list):
    url = 'http://192.168.10.102:5000/register/python'

    myobj = {
        "length": len(user_list),
        "payload": user_list,
    }

    req = requests.post(url, json=myobj)
    response = json.loads(req.text)

    if response['success'] == True:
        print(f"{bcolors.OKGREEN}{req.text}{bcolors.ENDC}")
        return True
    else:
        print(f"{bcolors.FAIL}{req.text}{bcolors.ENDC}")
        return False

def getExistingUserList():
    url = "http://192.168.10.102:5000/register/all"
    req = requests.get(url)
    res = json.loads(req.text)

    return_list = []

    for user in res['message']:
        return_list.append(user['name'])

    return return_list

if __name__ == "__main__":
    clear()

    print(f"{bcolors.HEADER}Start{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Reading CSV{bcolors.ENDC}")
    print()

    csv_file = getCSV()
    existing_users = getExistingUserList()

    with open(csv_file, 'r') as file:
        csvreader = csv.reader(file)

        next(csvreader) ## Skip header row

        user_list_to_bulk_add = []
        
        for row in csvreader:
            if row[0] not in existing_users:
                print(f"{bcolors.OKCYAN}Registering {row[0]}{bcolors.ENDC}")
                user_list_to_bulk_add.append([row[0], row[1]])
            else:
                print(f"{bcolors.WARNING}{row[0]} already exists...{bcolors.ENDC}")

        add_success = bulkAddToDb(user_list_to_bulk_add)

    print()

    if add_success == True:
        print(f"{bcolors.HEADER}Success. Users added to Database.{bcolors.ENDC}")
    else:
        print(f"Something went wrong while adding users to the database.")