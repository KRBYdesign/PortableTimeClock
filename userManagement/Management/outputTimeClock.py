from os import name, system
import requests
import json
import datetime
import csv
from random import randint

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

def Clear():
    system("cls" if name=="nt" else "clear")

def getAllRecordsFromTimeClock():
    print(f"{bcolors.OKCYAN}Fetching records from time clock...{bcolors.ENDC}")
    res = requests.get(f"http://{IP}:{PORT}/manage/all-time")
    parsedRequest = json.loads(res.text)

    return parsedRequest['payload']

def convert24hrFormat(time):
    split_time = str(time).replace(" AM", "").replace(" PM", "").split(":")
    
    if str(time).endswith(" PM"):
        split_time[0] = str(int(split_time[0]) + 12)

    if len(split_time[0]) < 2:
        split_time[0] = f"0{split_time[0]}"

    rejoined_time = ":".join(split_time)

    return rejoined_time

def convertDateAndTimeToEpoch(in_date, in_time):
    time_string = f"{in_date} {in_time}"
    timestamp = datetime.datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S")
    
    return timestamp

def appendShiftDurations(all_records):
    for record in all_records:
        if record['action'] == "IN":
            in_time = record['timestamp']
            out_time = getMatchingOutTime(record['shift_id'], all_records)

            duration = getTimeDifference(in_time, out_time)
            record['duration'] = str(duration)

def matchShift(number, shift_id, all_records):
    prev_shifts = []
    for record in all_records:
        if record['action'] == "OUT":
            if record['shift_id'] == "NULL" and record['number'] == number:
                if shift_id not in prev_shifts:
                    record['shift_id'] = shift_id
                    prev_shifts.append(shift_id)

def appendShiftNumbers(all_records):
    prev_shift_nums = []
    for record in all_records:
        record['shift_id'] = "NULL"

    for record in all_records:
        shift_id = random_with_N_digits(10)

        if record['action'] == "IN":
            if record['shift_id'] == "NULL":
                if shift_id not in prev_shift_nums:
                    record['shift_id'] = shift_id
                    matchShift(record['number'], shift_id, all_records)
                    prev_shift_nums.append(shift_id)

def getTimeDifference(in_time, out_time):
    if out_time == None:
        ## If the user did not clock out for what ever reason, set their clock out
        ## time to precisely 1am on October 22, the official end of all shifts.

        out_time = datetime.datetime.strptime("10/22/2023 01:00:00", "%m/%d/%Y %H:%M:%S")
    
    duration = out_time - in_time

    return duration

def getMatchingOutTime(shift_id, all_records):
    # Will return None if no matching out shift is able to be located.
    for record in all_records:
        if record['action'] == "OUT":
            if record['shift_id'] == shift_id:
                return record['timestamp']

def appendNames(all_records):
    url = f"http://{IP}:{PORT}/manage/all-users"
    res = requests.get(url)
    parsedRes = json.loads(res.text)
    payload = parsedRes['payload']

    for record in payload:
        for row in all_records:
            if record['number'] == row['number']:
                row['name'] = record['name']

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(range_start, range_end))

def getRecordNotes(number, all_records):
    notes = []

    return notes

if __name__ == "__main__":
    Clear()

    print(f"{bcolors.HEADER}Starting...{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Establishing Connection...{bcolors.ENDC}")

    ## Check that server is on and running
    try:
        result = requests.get(f"http://{IP}:{PORT}/manage")
        print(f"{bcolors.OKGREEN}Connection Established{bcolors.ENDC}")
    except requests.exceptions.RequestException as err:
        print(f"{bcolors.WARNING}Server is not responding. Ensure server is active.\n\n{bcolors.FAIL}ERROR: {err}\n\n{bcolors.WARNING}Exiting...{bcolors.ENDC}")
        quit(2)
    except:
        print(f"{bcolors.FAIL}Something went wrong establishing connection to the server.{bcolors.ENDC}")
        quit(2)


    all_records = getAllRecordsFromTimeClock()

    if not all_records:
        quit()
    else:
        print(f"{bcolors.OKGREEN}Success{bcolors.ENDC}")
    
    print(f"{bcolors.OKCYAN}Converting dates and times...{bcolors.ENDC}")
    for record in all_records:
        record["time"] = convert24hrFormat(record["time"])
        record["timestamp"] = convertDateAndTimeToEpoch(record["date"], record["time"])
    print(f"{bcolors.OKGREEN}Done{bcolors.ENDC}")

    print(f"{bcolors.OKCYAN}Matching shift numbers...{bcolors.ENDC}")
    appendShiftNumbers(all_records)
    print(f"{bcolors.OKGREEN}Done{bcolors.ENDC}")

    print(f"{bcolors.OKCYAN}Calculating shift durations...{bcolors.ENDC}")
    appendShiftDurations(all_records)
    print(f"{bcolors.OKGREEN}Done{bcolors.ENDC}")

    appendNames(all_records)
    
    with open("timeclock_output.csv", 'w') as output_file:
        csv_writer = csv.writer(output_file)

        csv_writer.writerow(["Shift Num", "ID", "Name", "Duration", "Notes"])
        for record in all_records:
            if record['action'] == "IN":
                notes = getRecordNotes(record['number'], all_records)
                if len(notes) == 0:
                    notes = ""

                try:
                    csv_writer.writerow([record['shift_id'], record['number'], record['name'], record['duration'], notes])
                except KeyError:
                    csv_writer.writerow([record['shift_id'], record['number'], record['name'], "NULL", notes])


    print(f"{bcolors.HEADER}Success: timeclock_output.csv has been created.")
