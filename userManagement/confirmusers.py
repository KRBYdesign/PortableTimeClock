from os import name, system
import csv
from random import randint
import requests
from datetime import date
import json

IP = "192.168.10.102"
PORT = 5000

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

CSV_FILE_NAME = "TNTStationSheet - Sheet1.csv"
OUTPUT_FILE_NAME = f"ConfirmedUsersWithIdsAndLinks_{date.today()}.csv"

def clear():
    system("cls" if name == "nt" else "clear")

def getConfirmedGuards():
    confirmed = []
    with open(CSV_FILE_NAME, 'r') as csv_file:
        csvreader = csv.reader(csv_file)

        for row in csvreader:
            if not (row[0] == ""):
                if (row[4] == "TRUE") or (row[3] == "TRUE"):
                    confirmed.append(row)

    return confirmed

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(range_start, range_end))

def getDbNumbers():
    url = f"http://{IP}:{PORT}/register/all"
    res = requests.get(url)
    prevNumbers = []

    resList = str(res.text).split("},{")

    if "number" in str(resList):
        for row in resList:
            row = row.split(",")
            prevNumbers.append(str(row[1]).replace('"number":', ""))
    else:
        pass

    return prevNumbers

def generateGuardIds(confirmedGuards):
    print(confirmedGuards[0])

    for guard in confirmedGuards:
        if len(guard) < 9:
            new_number = random_with_N_digits(9)
            guard.append(new_number)

    return confirmedGuards

def generateIndividualLink(name, id):
    name = str(name).replace(" ", "%20")
    individual_link = f"https://tntsecuritysolutions.lacoxconsulting.com/AtTheStation/MyId?name={name}&id={id}"

    print(f"{bcolors.OKBLUE} --> {individual_link}{bcolors.ENDC}")

    return individual_link

def cleanNames(list):
    for row in list:
        row[0] = str(row[0]).replace(" **", "").replace("'", "")
    return list

def assignGuardGroups(confirmedGuards):
    for row in confirmedGuards:
        if len(str(row[8])) < 10:
            if str(row[6]).startswith("6:"):
                row[8] = row[8] + "A"
            elif str(row[6]).startswith("8:"):
                row[8] = row[8] + "B"
            elif str(row[6]).startswith("9:30"):
                row[8] = row[8] + "C"
            elif str(row[6]).startswith("9:45"):
                row[8] = row[8] + "D"
            elif str(row[6]).startswith("10:00"):
                row[8] = row[8] + "E"
            elif str(row[6]).startswith("10:30"):
                row[8] = row[8] + "F"
            elif str(row[6]).startswith("12:30"):
                row[8] = row[8] + "G"
            elif str(row[6]).startswith("1 "):
                row[8] = row[8] + "H"
            elif str(row[6]).startswith("7 "):
                row[8] = row[8] + "I"
            else:
                # "Z" denotes the user was not assigned to a group at the time this list
                # was confirmed and the users were added to the database.

                row[8] = row[8] + "Z"

    return confirmedGuards

def getAndAttachExistingIds(confirmedGuards):
    url = "http://192.168.10.102:5000/register/all"
    res = requests.get(url)
    parsedRes = json.loads(res.text)
    
    for user in parsedRes['message']:
        for guard in confirmedGuards:
            if user['name'] == guard[0]:
                guard.append(user['number'])

    return confirmedGuards

if __name__ == "__main__":
    clear()

    # Get Guards from CSV
    print(f"{bcolors.OKCYAN}Getting all confirmed personnel...{bcolors.ENDC}")
    confirmedGuards = getConfirmedGuards()
    print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")

    # Clean CSV Names
    print(f"{bcolors.OKCYAN}Sanitizing inputs...{bcolors.ENDC}")
    confirmedGuards = cleanNames(confirmedGuards)
    print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")

    # Get Guard ID's for all existing Guards
    confirmedGuards = getAndAttachExistingIds(confirmedGuards)

    # Generate Guard ID's for guards without previously existing ID
    print(f"{bcolors.OKCYAN}Generating unique ID numbers...{bcolors.ENDC}")
    confirmedGuards = generateGuardIds(confirmedGuards)
    print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")

    guardLinks = []

    print(f"{bcolors.OKCYAN}Assigning groups...{bcolors.ENDC}")
    confirmedGuards = assignGuardGroups(confirmedGuards)
    print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")

    ## Generate Links
    print(f"{bcolors.OKCYAN}Generating individual links...{bcolors.ENDC}")
    for guard in confirmedGuards:   
        guardLinks.append(generateIndividualLink(guard[0], guard[8]))
    print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")

    ## Attach individual links to each guard's row
    print(f"{bcolors.OKCYAN}Attaching links...{bcolors.ENDC}")
    for index, row in enumerate(confirmedGuards):
        row.append(guardLinks[index])
    print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")

    print(f"{bcolors.OKCYAN}Generating Output.csv...{bcolors.ENDC}")
    with open(OUTPUT_FILE_NAME, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["Name", "ID", "Email", "Shift Time", "Link"])
        for index, row in enumerate(confirmedGuards):
            writer.writerow([row[0], row[8], row[2], row[6], row[9]])
    print(f"{bcolors.HEADER}SUCCESS: Output.csv created.{bcolors.ENDC}")