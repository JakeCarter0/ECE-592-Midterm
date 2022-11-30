"""
Created on June 8 2022

@author: Jake Carter
PiE Midterm file 2:
Includes code for manipulating membership data held in membershipdata.csv
Requires pynput, matplotlib, and numpy
"""


import re
import datetime
import csv
import sys
import os
import threading
import shutil
import tempfile
import copy
import argparse
try:
    import pynput
except:
    print("Warning: [pynput] library not installed, install with 'pip install pynput'")
    sys.exit(-1)
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: [matplotlib] library not installed, install with 'pip install matplotlib'")
    sys.exit(-1)
try:
    import numpy as np
except:
    print("Warning: [numpy] library not installed, install with 'pip install numpy'")
    sys.exit(-1)


# with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     # try:
#
#         listener.start()
    # except MyException:
    #     print("Exception")
    #     quit()

command = "q"


def on_press(key):
    if key == pynput.keyboard.Key.esc:
        if command == "b":
            escIn = 1
        elif command == "q":
            print("\nQuiting program...")
            os._exit(1)
        elif command == "r":
            print("\nRestarting program...")
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

        # raise MyException(key)

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        quit()
# escapeThread = threading.Thread(target = escape)




def getMember(search:int = 0):
    fieldnames = ["Mno", "First name", "MI", "Last name", "DoB", "Address", "Status", "msd", "med", "rdate", "Phone", "Email", "Notes"]
    findMember = list()
    while True:
        try:
            findMember = list()
            inputs = str(input("Enter target member attribute(s) (enter \"help\" for list of attributes): "))
            mno = re.search("Mno:\s*([\d]+)", inputs)
            if mno:
                findMember.append(("Mno", mno.group(1)))
            name = re.search("Name:\s*([\w-]+)\s*([\w-]*)\s*([\w-]*)", inputs)
            if name:
                for i in name.groups():
                    if i != "":
                        findMember.append(("Name", i))
            dob = re.search("DoB:\s*([\d\s]+)", inputs)
            if dob:
                try:
                    findMember.append(("DoB", datetime.datetime.strptime(dob.group(1), "%m %d %Y").strftime("%B %d %Y")))
                except ValueError:
                    try:
                        findMember.append(("DoB", datetime.datetime.strptime(dob.group(1), "%B %d %Y").strftime("%B %d %Y")))
                    except ValueError:
                        print("Warning: invalid DoB format. Please enter as: mm dd yyyy")
            addr = re.search("Address:\s*([\w\s\d-]+)", inputs)
            if addr:
                findMember.append(("Address", addr.group(1)))
            stat = re.search("Status: \s*([\w]+)", inputs)
            if stat:
                if stat.group(1) == "Basic" or stat.group(1) == "Silver" or stat.group(1) == "Gold" or stat.group(1) == "Platinum" or stat.group(1) == "None":
                    findMember.append(("Status", stat.group(1)))
                else:
                    print("WARNING: : invalid Status format. Please enter: Basic, Silver, Gold, Platinum, or None")
            msd = re.search("msd:\s*([\d\s]+)", inputs)
            if msd:
                try:
                    findMember.append(("msd", datetime.datetime.strptime(msd.group(1), "%m %d %Y").strftime("%B %d %Y")))
                except ValueError:
                    try:
                        findMember.append(("msd", datetime.datetime.strptime(msd.group(1), "%B %d %Y").strftime("%B %d %Y")))
                    except ValueError:
                        print("Warning: invalid msd format. Please enter as: mm dd yyyy")
            med = re.search("med:\s*([\d\s]+)", inputs)
            if med:
                try:
                    findMember.append("med", datetime.datetime.strptime(med.group(1), "%m %d %Y").strftime("%B %d %Y"))
                except ValueError:
                    try:
                        findMember.append(("med", datetime.datetime.strptime(med.group(1), "%B %d %Y").strftime("%B %d %Y")))
                    except ValueError:
                        print("Warning: invalid med format. Please enter as: mm dd yyyy")
            rdate = re.search("rdate:\s*([\d\s]+)", inputs)
            if rdate:
                try:
                    findMember.append(("rdate", datetime.datetime.strptime(rdate.group(1), "%m %d %Y").strftime("%B %d %Y")))
                except ValueError:
                    try:
                        findMember.append(("rdate", datetime.datetime.strptime(rdate.group(1), "%B %d %Y").strftime("%B %d %Y")))
                    except ValueError:
                        print("Warning: invalid rdate format. Please enter as: mm dd yyyy")
            phone = re.search("Phone:\s*([\d]+)", inputs)
            if phone:
                findMember.append(("Phone", phone.group(1)))
            email = re.search("Email:\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", inputs)
            if email:
                findMember.append(("Email", email.group(1)))
            notes = re.search("Notes:\s*([\d\s\w]+)", inputs)
            if notes:
                findMember.append(("Notes", notes.group(1)))
            if inputs == "help":
                print("Valid member attributes:")
                print("Mno: (6 digit membership number)")
                print("Name: (First, middle, and/or last names seperated by spaces)(Eg: \"Name: Jake\" or \"Name: Jake Carter\")")
                print("DoB: (mm dd yyyy format date of birth)")
                print("Address: (Address string)")
                print("Status: (Basic, Silver, Gold, Platinum, None)")
                print("msd: (mm dd yyyy format membership start date)")
                print("med: (mm dd yyyy format membership end date)")
                print("rdate: (mm dd yyyy format membership renewal date)")
                print("Phone: (10 digit phone number #########)")
                print("Email: (Email address string)")
                print("Notes: (Notes string)")
                print("Example: \"Name: Jake Carter, Status: Silver, Phone: 1234567890\"")
                continue
            if len(findMember) > 0:
                print("Searching for members...")
                print(findMember)
            else:
                print("No valid attributes entered.")
                continue
        except:
            print("Invalid entry")
            continue
        possibleMatches = list()
        if len(findMember) < 1:
            print("Error: no valid attributes entered")
            continue
        with open("memberdata.csv", "r", newline = "") as fr:
            reader = csv.DictReader(fr)
            if findMember[0][0] == "Name":
                for row in reader:
                    if row["First name"] == findMember[0][1] or row["MI"] == findMember[0][1] or row["Last name"] == findMember[0][1]:
                        possibleMatches.append(row)
            else:
                for row in reader:
                    if row[findMember[0][0]] == findMember[0][1]:
                        possibleMatches.append(row)
        # for member in possibleMatches:
        #     print(member)
        if len(findMember) > 1:
            # print(findMember[1:])
            for attribute in findMember[1:]:
                tempMatches = list()
                # print(attribute)
                if attribute[0] == "Name":
                    for member in possibleMatches:
                        if member["First name"] == attribute[1] or member["MI"] == attribute[1] or member["Last name"] == attribute[1]:
                            tempMatches.append(member)
                else:
                    for member in possibleMatches:
                        # print("Testing: {}" .format(member))
                        if member[attribute[0]] == attribute[1]:
                            # print("Fail")
                            tempMatches.append(member)
                        # else:
                        #     print("Pass")
                possibleMatches = tempMatches
        if len(possibleMatches) < 1:
            print("No matches found")
            continue
        if len(possibleMatches) > 10:
            while True:
                conf = str(input("Over 10 matching members found. Continue? (y/n): "))
                if conf == "y" or conf == "n" :
                    break
                else:
                    print("Please enter \"y\" or \"n\"")
            if conf == "n":
                continue
        if search == 0:
            if len(possibleMatches) > 1:
                print("Please select target member:\n")
                for i in range(0, len(possibleMatches)):
                    print("Member [{}]:" .format(i))
                    print(possibleMatches[i])

                while True:
                    try:
                        selection = int(input("Please enter selection (0 - {}): " .format(len(possibleMatches) - 1)))
                        if selection < 0 or selection > (len(possibleMatches) - 1):
                            print("Invalid selection")
                            continue
                    except:
                        print("Invalid foramt")
                        continue
                    print("Target: {}" .format(possibleMatches[selection]))
                    while True:
                        conf = str(input("Continue? (y/n): "))
                        if conf == "y" or conf == "n" :
                            break
                        else:
                            print("Please enter \"y\" or \"n\"")
                    break
                if conf == "n":
                    continue
                else:
                    break
            else:
                print("Target: {}" .format(possibleMatches[0]))
                while True:
                    conf = str(input("Continue? (y/n): "))
                    if conf == "y" or conf == "n" :
                        break
                    else:
                        print("Please enter \"y\" or \"n\"")
                if conf == "n":
                    continue
                else:
                    selection = 0
                    break
        else:
            for i in range(0, len(possibleMatches)):
                if len(possibleMatches) > 1:
                    print("Member [{}]:" .format(i))
                print(possibleMatches[i])
            while True:
                conf = str(input("Search another? (y/n): "))
                if conf == "y" or conf == "n" :
                    break
                else:
                    print("Please enter \"y\" or \"n\"")
            if conf == "y":
                continue
            else:
                break

    if search == 0:
        targetMember = possibleMatches[selection]
        return targetMember
    else:
        return 0
    #     editedMember = copy.deepcopy(targetMember)
    #     editedMember["Status"] = "None"
    #     editedMember["med"] = datetime.datetime.today().strftime("%B %d %Y")
    #     print("Target:")
    #     print(list(targetMember.values()))
    #     print("New:")
    #     print(list(editedMember.values()))
    #
    #
    #     break
    # tempwrite = tempfile.NamedTemporaryFile("w+t", newline = "", delete = False)
    # with open("memberdata.csv", "r", newline = "") as fr, tempwrite:
    #     reader = csv.reader(fr)
    #     writer = csv.writer(tempwrite)
    #     print("Searching...")
    #     for row in reader:
    #         # print(row)
    #         if row == list(targetMember.values()):
    #             writer.writerow(list(editedMember.values()))
    #             print("Found!!")
    #         else:
    #             writer.writerow(row)
    # shutil.move(tempwrite.name, "memberdata.csv")

def replaceMember(targetMember:dict, editedMember:dict):
    tempwrite = tempfile.NamedTemporaryFile("w+t", newline = "", delete = False)
    with open("memberdata.csv", "r", newline = "") as fr, tempwrite:
        reader = csv.reader(fr)
        writer = csv.writer(tempwrite)
        print("Searching...")
        print("Target: {}" .format(targetMember))
        print("New: {}" .format(editedMember))
        for row in reader:
            # print(row)
            if row == list(targetMember.values()):
                writer.writerow(list(editedMember.values()))
                print("Done")
            else:
                writer.writerow(row)
    shutil.move(tempwrite.name, "memberdata.csv")

def addMember():
    fieldnames = ["Mno", "First name", "MI", "Last name", "DoB", "Address", "Status", "msd", "med", "rdate", "Phone", "Email", "Notes"]
    newMember = {"Mno" : "", "First name" : "", "MI" : "", "Last name" : "", "DoB" : "", "Address" : "", "Status" : "", "msd" : "", "med" : "", "rdate" : "", "Phone" : "", "Email" : "", "Notes" : ""}
    print("Adding new member, please enter following information:")
    while True:

        while True:
            try:
                fName = str(input("First Name: "))
                if fName == "":
                    print("First Name is required")
                    continue
                elif re.search("^[a-zA-Z-]+", fName).group(0) != fName:
                    print('Invalid entry, no special characters or numbers')
                    continue
                else:
                    newMember["First name"] = fName
                    break
            except ValueError:
                print("Invalid entry, please enter a string")
                continue

        while True:
            try:
                mName = str(input("Middle Name: "))
                if fName == "":
                    break
                elif re.search("^[a-zA-Z-]+", mName).group(0) != mName:
                    print('Invalid entry, no special characters or numbers')
                    continue
                else:
                    newMember["MI"] = mName
                    break
            except ValueError:
                print("Invalid entry, please enter a string")
                continue

        while True:
            try:
                lName = str(input("Last Name: "))
                if lName == "":
                    print("Last Name is required")
                    continue
                elif re.search("^[a-zA-Z-]+", lName).group(0) != lName:
                    print("Invalid entry, no special characters or numbers")
                    continue
                else:
                    newMember["Last name"] = lName
                    break
            except ValueError:
                print("Invalid entry, please enter a string")
                continue

        while True:
            try:
                dobStr = str(input("Date of birth (mm dd yyyy): "))
                if dobStr == "":
                    print("Date of birth is required")
                    continue
                else:
                    dob = datetime.datetime.strptime(dobStr, "%m %d %Y")
                    if datetime.date.today().year - dob.year - ((datetime.datetime.today().month, datetime.datetime.today().day) < (dob.month, dob.day)) < 18:
                        print("Invalid entry, all members must be over 18 years old")
                        continue
                    newMember["DoB"] = dob.strftime("%B %d %Y")
                    break
            except ValueError:
                print("Invalid entry, please enter date as mm dd yyyy")
                continue

        mno = 0
        try:
            with open("memberdata.csv", "r") as fr:
                reader = csv.DictReader(fr)
                for row in reader:
                    if fName == row["First name"] and mName == row["MI"] and lName == row["Last name"] and newMember["DoB"] == row["DoB"]:
                        print("Error, member already in system")
                        break
                    elif int(row["Mno"]) >= mno:
                        mno = int(row["Mno"]) + 1
                else:

                    break
                continue
        except FileNotFoundError:
            with open("memberdata.csv", "w", newline = "") as fw:
                writer = csv.DictWriter(fw, fieldnames = fieldnames)
                writer.writeheader()
            break
    newMember["Mno"] = mno
    while True:
        try:
            addr = str(input("Address: "))
            if addr == "":
                break
            elif re.search("^[a-zA-Z0-9-,. ]+", addr).group(0) != addr:
                print("Invalid entry, no special characters besides \"-\" and \",\"")
                continue
            else:
                newMember["Address"] = addr
                break
        except ValueError:
            print("Invalid entry, please enter a string")
            continue



    while True:
        try:
            msdStr = str(input("Membership start date (mm dd yyyy): "))
            if msdStr == "":
                msd = datetime.datetime.today()
                break
            else:
                msd = datetime.datetime.strptime(msdStr, "%m %d %Y")
                if msd.year - dob.year - ((msd.month, msd.day) < (dob.month, dob.day)) < 18:
                    print("Invalid entry, all members must be over 18 years old to begin membership")
                    continue
                elif msd > datetime.datetime.today():
                    print("Invalid entry, membership can not start in the future")
                    continue
                newMember["msd"] = msd.strftime("%B %d %Y")
                break
        except ValueError:
            print("Invalid entry, please enter date as mm dd yyyy")
            continue

    while True:
        try:
            medStr = str(input("Membership end date (mm dd yyyy)(leave blank for current member): "))
            if medStr == "":
                break
            else:
                med = datetime.datetime.strptime(medStr, "%m %d %Y")
                if msd > med:
                    print("Invalid entry, membership can not end before membership start date")
                    med = None
                    continue
                elif med > datetime.datetime.today():
                    print("Invalid entry, leave field blank for memberships that have not ended")
                    med = None
                    continue
                newMember["med"] = med.strftime("%B %d %Y")
                newMember["Status"] = "None"
                break
        except ValueError:
            print("Invalid entry, please enter date as mm dd yyyy")
            continue

    while True:
        try:
            rdateStr = str(input("Membership renewal date (mm dd yyyy): "))
            if rdateStr == "":
                rdate = datetime.datetime.today() + datetime.timedelta(days = 365)
            else:
                rdate = datetime.datetime.strptime(rdateStr, "%m %d %Y")
                if rdate < datetime.datetime.today():
                    print("Invalid entry, renewal date must be in the future")
                    continue
                elif rdate.year - datetime.datetime.today().year - ((rdate.month, rdate.day) < (datetime.datetime.today().month, datetime.datetime.today().day)) >= 5:
                    print("Invalid entry, renewal date must be at most 5 years in the future")
                    continue
            newMember["rdate"] = rdate.strftime("%B %d %Y")
            break
        except ValueError:
            print("Invalid entry, please enter date as mm dd yyyy")
            continue

    if newMember["med"] == "":
        while True:
            try:
                status = str(input("Status (Basic, Silver, Gold, Platinum): "))
                if status == "":
                    print("Status required")
                    continue
                elif status != "Basic" and status != "Silver" and status != "Gold" and status != "Platinum":
                    print('Invalid entry, select a valid status')
                    continue
                else:
                    newMember["Status"] = status
                    break
            except ValueError:
                print("Invalid entry, please enter a string")
                continue
    else:
        newMember["Status"] = "None"

    while True:
        try:
            phone = int(input("Phone number: "))
            if phone == "":
                print("Phone number is required")
                continue
            elif phone < 0 or phone > 9999999999:
                print("Invalid entry, please enter a 10 digit phone number")
                continue
            newMember["Phone"] = phone
            break
        except ValueError:
            print("Invalid entry, please enter an integer")
            continue

    while True:
        try:
            email = str(input("Email address: "))
            if email == "":
                break
            elif  re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email).group(0) != email:
                print("Invalid entry, please enter a valid email address")
                continue
            newMember["Email"] = email
            break
        except ValueError:
            print("Invalid entry, please enter a string")
            continue
        except AttributeError:
            print("Invalid entry, please enter a valid email address")
            continue

    while True:
        try:
            notes = str(input("Notes: "))
            if notes == "":
                break
            newMember["Notes"] = notes
            break
        except ValueError:
            print("Invalid entry, please enter a string")
            continue
    print(newMember)
    with open("memberdata.csv", "a", newline = "") as fw:
        writer = csv.DictWriter(fw, fieldnames = fieldnames)
        writer.writerow(newMember)

def removeMember():
    print("Removing member")
    targetMember = getMember()
    editedMember = copy.deepcopy(targetMember)
    editedMember["Status"] = "None"
    editedMember["med"] = datetime.datetime.today().strftime("%B %d %Y")

    replaceMember(targetMember = targetMember, editedMember = editedMember)

def changeStatus():
    print("Changing member status")
    targetMember = getMember()
    while True:
        status = str(input("Enter new status (Basic, Silver, Gold, Platinum): "))
        if status != "Basic" and status != "Silver" and status != "Gold" and status != "Platinum":
            print("Invalid entry")
            continue
        elif status == targetMember["Status"]:
            print("Target member already has {} status" .format(status))
            while True:
                try:
                    conf = str(input("Choose diffrent status? (y/n): "))
                    if conf == "y" or conf == "n":
                        break
                    else:
                        print("Please enter \"y\" or \"n\"")
                except:
                    print("Invalid entry")
            if conf == "y":
                continue
            else:
                break
        else:
            break
    editedMember = copy.deepcopy(targetMember)
    if targetMember["Status"] == "None":
        editedMember["med"] = ""
    editedMember["Status"] = status
    editedMember["rdate"] = (datetime.datetime.today() + datetime.timedelta(days = 365)).strftime("%B %d %Y")
    print("replacing...")

    replaceMember(targetMember = targetMember, editedMember = editedMember)

def modifyData():
    fieldnames = ["Mno", "First name", "MI", "Last name", "DoB", "Address", "Status", "med", "rdate", "Phone", "Email", "Notes"]
    print("Modifying data")
    targetMember = getMember()
    editedMember = copy.deepcopy(targetMember)
    while True:
        try:
            attr = str(input("Enter target attribute: "))
            if attr not in fieldnames:
                print("Invalid attribute")
                print("Valid attributes: {}" .format(fieldnames))
            else:
                break
        except:
            print("Invalid entry")
    while True:
        try:
            entry = str(input("Enter new {}: " .format(attr)))
        except:
            print("Invalid entry")
            continue
        if attr == "Mno":
            try:
                if int(entry) < 0 or int(entry) > 999999:
                    print("Mno must be a 6 digit positive number")
                    continue
            except ValueError:
                print("Mno must be a 6 digit positive number")
                continue
            with open("memberdata.csv", "r", newline = "") as fr:
                reader = csv.DictReader(fr)
                for row in reader:
                    if entry == row["Mno"]:
                        print("{} already assigned to member" .format(entry))
                        break
                else:
                    break
                continue
        if attr == "First name":
            try:
                if re.search("^[a-zA-Z-]+", entry).group(0) != entry:
                    print('Invalid entry, no special characters or numbers')
                    continue
            except:
                print("Invalid entry")
            with open("memberdata.csv", "r") as fr:
                reader = csv.DictReader(fr)
                for row in reader:
                    if entry == row["First name"] and targetMember["MI"] == row["MI"] and targetMember["Last name"] == row["Last name"] and targetMember["DoB"] == row["DoB"]:
                        print("Error, member already in system")
                        break
                else:
                    break
                continue
        if attr == "MI":
            try:
                if re.search("^[a-zA-Z-]+", entry).group(0) != entry:
                    print('Invalid entry, no special characters or numbers')
                    continue
            except:
                print("Invalid entry")
            with open("memberdata.csv", "r") as fr:
                reader = csv.DictReader(fr)
                for row in reader:
                    if targetMember["First name"] == row["First name"] and entry == row["MI"] and targetMember["Last name"] == row["Last name"] and targetMember["DoB"] == row["DoB"]:
                        print("Error, member already in system")
                        break
                else:
                    break
                continue
        if attr == "Last name":
            try:
                if re.search("^[a-zA-Z-]+", entry).group(0) != entry:
                    print('Invalid entry, no special characters or numbers')
                    continue
            except:
                print("Invalid entry")
            with open("memberdata.csv", "r") as fr:
                reader = csv.DictReader(fr)
                for row in reader:
                    if targetMember["First name"] == row["First name"] and targetMember["MI"] == row["MI"] and entry == row["Last name"] and targetMember["DoB"] == row["DoB"]:
                        print("Error, member already in system")
                        break
                else:
                    break
                continue
        if attr == "DoB":
            try:
                entry = datetime.datetime.strptime(entry, "%m %d %Y")
                msdCheck = datetime.datetime.strptime(targetMember["msd"], "%B %d %Y")
                if msdCheck.year - entry.year - ((msdCheck.month, msdCheck.day) < (entry.month, entry.day)) < 18:
                    print("Invalid Input, all members must be over 18 years old")
                    continue
                entry = entry.strftime("%B %d %Y")
            except:
                print("Invalid input, please enter date as mm dd yyyy")
                continue
            with open("memberdata.csv", "r") as fr:
                reader = csv.DictReader(fr)
                for row in reader:
                    if targetMember["First name"] == row["First name"] and targetMember["MI"] == row["MI"] and targetMember["Last name"] == row["Last name"] and entry == row["DoB"]:
                        print("Error, member already in system")
                        break
                else:
                    break
                continue
        if attr == "Address":
            try:
                if re.search("^[a-zA-Z0-9-,. ]*", entry).group(0) != entry:
                    print("Invalid entry, no special characters besides \"-\" and \",\"")
                    continue
                else:
                    break
            except:
                print("Invalid entry")
        if attr == "Status":
            if entry != "Basic" and entry != "Silver" and entry != "Gold" and entry != "Platinum" and entry != "None":
                print("Invalid entry, please enter: (Basic, Silver, Gold, Platinum, None)")
            elif entry == "None":
                if targetMember["med"] == "":
                    editedMember["med"] = datetime.datetime.today().strftime("%B %d %Y")
                break

            else:
                if targetMember["med"] != "":
                    editedMember["med"] = ""
                break

        if attr == "med":
            if entry != "":
                try:
                    entry = datetime.datetime.strptime(entry, "%m %d %Y")
                    if datetime.datetime.strptime(targetMember["msd"], "%B %d %Y") > entry:
                        print("Invalid Input, membership can not end before membership start date")
                        continue
                    elif entry > datetime.datetime.today():
                        print("Invalid Input, membership can end in the future")
                        continue
                    else:
                        entry = entry.strftime("%B %d %Y")
                        editedMember["Status"] = "None"
                        break
                except:
                    print("Invalid input, please enter date as mm dd yyyy")
            elif targetMember["Status"] == "None":
                while True:
                    try:
                        status = str(input("Enter new status (Basic, Silver, Gold, Platinum): "))
                        if status != "Basic" and status != "Silver" and status != "Gold" and status != "Platinum":
                            print("Invalid entry")
                            continue
                        else:
                            break
                    except:
                        print("Invalid entry")
                        continue
                editedMember["Status"] = status
                break
        if attr == "rdate":
            try:
                entry = datetime.datetime.strptime(entry, "%m %d %Y")
                if entry < datetime.datetime.today():
                    print("Invalid Input, renewal date must be in the future")
                    continue
                elif entry.year - datetime.datetime.today().year - ((entry.month, entry.day) < (datetime.datetime.today().month, datetime.datetime.today().day)) >= 5:
                    print("Invalid entry, renewal date must be at most 5 years in the future")
                    continue
                else:
                    entry = entry.strftime("%B %d %Y")
                    break
            except:
                print("Invalid input, please enter date as mm dd yyyy")
        if attr == "Phone":
            try:
                if int(entry) < 0 or int(entry) > 9999999999:
                    print("Invalid entry, please enter a 10 digit phone number")
                    continue
                else:
                    break
            except ValueError:
                print("Invalid entry, please enter a 10 digit phone number")
                continue
        if attr == "Email":
            try:
                if re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", entry).group(0) != entry:
                    print("Invalid entry, please enter a valid email address")
                    continue
                else:
                    break
            except:
                print("Invalid entry, please enter a valid email address")
        if attr == "Notes":
            True

    editedMember[attr] = entry
    replaceMember(targetMember = targetMember, editedMember = editedMember)

def importData():
    fieldnames = ["Mno", "First name", "MI", "Last name", "DoB", "Address", "Status", "msd", "med", "rdate", "Phone", "Email", "Notes"]
    acceptedMembers = list()
    invalidAttr = list()
    missingAttr = list()
    while True:
        sourceFile = str(input("Please enter text or csv file name: "))
        try:
            with open(sourceFile, "r", newline = "") as newData:
                reader = csv.DictReader(newData)
                for row in reader:
                    newMember = copy.deepcopy(row)
                    try:
                        if row["First name"] == "":
                            # print("1")
                            missingAttr.append(newMember)
                            continue
                        elif re.search("^[a-zA-Z-]+", row["First name"]).group(0) != row["First name"]:
                            invalidAttr.append(newMember)
                            # print("2")
                            continue
                        elif re.search("^[a-zA-Z-]*", row["MI"]).group(0) != row["MI"]:
                            invalidAttr.append(newMember)
                            # print("3")
                            continue
                        elif row["Last name"] == "":
                            missingAttr.append(newMember)
                            # print("4")
                            continue
                        elif re.search("^[a-zA-Z-]+", row["Last name"]).group(0) != row["Last name"]:
                            invalidAttr.append(newMember)
                            # print("5")
                            continue
                        elif row["DoB"] == "":
                            missingAttr.append(newMember)
                            # print("6")
                            continue
                        elif row["Address"] != "" and re.search("^[a-zA-Z0-9-,. ]*", row["Address"]).group(0) != row["Address"]:
                            invalidAttr.append(newMember)
                            # print("7")
                            continue
                        elif row["Status"] == "":
                            missingAttr.append(newMember)
                            # print("8")
                            continue
                        elif row["Status"] != "Basic" and row["Status"] != "Silver" and row["Status"] != "Gold" and row["Status"] != "Platinum" and row["Status"] != "None":
                            invalidAttr.append(newMember)
                            # print("9")
                            continue
                        elif row["msd"] == "":
                            missingAttr.append(newMember)
                            # print("10")
                            continue
                        elif row["rdate"] == "":
                            missingAttr.append(newMember)
                            # print("11")
                            continue
                        elif row["Phone"] == "":
                            missingAttr.append(newMember)
                            # print("12")
                            continue
                        else:
                            if row["Email"] != "":
                                try:
                                    if re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*", row["Email"]).group(0) != row["Email"]:
                                        invalidAttr.append(newMember)
                                        # print("13")
                                        continue
                                except AttributeError:
                                    invalidAttr.append(newMember)
                                    # print("13")
                                    continue
                            try:
                                dob = datetime.datetime.strptime(row["DoB"], "%B %d %Y")
                                if datetime.date.today().year - dob.year - ((datetime.datetime.today().month, datetime.datetime.today().day) < (dob.month, dob.day)) < 18:
                                    invalidAttr.append(newMember)
                                    print(datetime.date.today().year - dob.year - ((datetime.datetime.today().month, datetime.datetime.today().day) < (dob.month, dob.day)))
                                    # print("14")
                                    continue
                            except ValueError:
                                invalidAttr.append(newMember)
                                # print("15")
                                continue
                            try:
                                msd = datetime.datetime.strptime(row["msd"], "%B %d %Y")
                                if msd.year - dob.year - ((msd.month, msd.day) < (dob.month, dob.day)) < 18:
                                    print(msd.year - dob.year - ((msd.month, msd.day) < (dob.month, dob.day)))
                                    invalidAttr.append(newMember)
                                    # print("16")
                                    continue
                                elif msd > datetime.datetime.today():
                                    invalidAttr.append(newMember)
                                    # print("17")
                                    continue
                            except ValueError:
                                invalidAttr.append(newMember)
                                # print("18")
                                continue
                            try:
                                rdate = datetime.datetime.strptime(row["rdate"], "%B %d %Y")
                                if rdate < datetime.datetime.today():
                                    invalidAttr.append(newMember)
                                    # print("19")
                                    continue
                                elif rdate.year - datetime.datetime.today().year - ((rdate.month, rdate.day) < (datetime.datetime.today().month, datetime.datetime.today().day)) >= 5:
                                    invalidAttr.append(newMember)
                                    # print("20")
                                    continue
                            except ValueError:
                                invalidAttr.append(newMember)
                                # print("21")
                                continue
                            try:
                                if int(row["Phone"]) < 0 or int(row["Phone"]) > 9999999999:
                                    invalidAttr.append(newMember)
                                    # print("22")
                                    continue
                            except (TypeError, ValueError):
                                invalidAttr.append(newMember)
                                # print("23")
                                continue
                            if row["Status"] == "None" and row["med"] == "":
                                missingAttr.append(newMember)
                                # print("24")
                                continue
                            if row["med"] != "":
                                if row["Status"] != "None":
                                    invalidAttr.append(newMember)
                                    # print("25")
                                    continue
                                try:
                                    med = datetime.datetime.strptime(row["med"], "%B %d %Y")
                                    if msd > med:
                                        invalidAttr.append(newMember)
                                        # print("26")
                                        continue
                                    elif med > datetime.datetime.today():
                                        invalidAttr.append(newMember)
                                        # print("27")
                                        continue
                                except ValueError:
                                    invalidAttr.append(newMember)
                                    # print("28")
                                    continue
                            try:
                                if int(row["Mno"]) < 0 or int(row["Mno"]) > 999999:
                                    invalidAttr.append(newMember)
                                    # print("29")
                                    continue
                            except TypeError:
                                invalidAttr.append(newMember)
                                # print("30")
                                continue
                    except AttributeError:
                            invalidAttr.append(newMember)
                            # print("31")
                            continue
                    acceptedMembers.append(newMember)
                break
                    # if row["First name"] == "" or row["Last name"] == "" or row["DoB"] == "" or row["Status"] == "" or row["msd"] == "" or row["rdate"] == "" or row["Phone"] == "":
                    #     deniedMembers.append(newMember)
        except FileNotFoundError:
            print("Error, {} not found" .format(sourceFile))
            continue
        except KeyError:
            print("Error, {} is not in the correct format")

    attrSet = set()
    checkMembers = copy.deepcopy(acceptedMembers)
    for member in checkMembers:
        if member["Mno"] in attrSet:
            acceptedMembers.remove(member)
            invalidAttr.append(member)
        elif member["First name"] + member["MI"] + member["Last name"] + member["DoB"] in attrSet:
            acceptedMembers.remove(member)
            invalidAttr.append(member)
        else:
            attrSet.add(member["Mno"])
            attrSet.add(member["First name"] + member["MI"] + member["Last name"] + member["DoB"])

    existingMembers = list()

    checkMembers = copy.deepcopy(acceptedMembers)
    with open("memberdata.csv", "r", newline = "") as fr:
        reader = csv.DictReader(fr)
        for row in reader:
            for member in checkMembers:
                if row["Mno"] == member["Mno"]:
                    acceptedMembers.remove(member)
                    existingMembers.append(member)
                elif row["First name"] == member["First name"] and row["MI"] == member["MI"] and row["Last name"] == member["Last name"] and row["DoB"] == member["DoB"]:
                    acceptedMembers.remove(member)
                    existingMembers.append(member)
        if len(existingMembers) > 0:
            print("{} members are already filed" .format(len(existingMembers)))
            while True:
                overwrite = str(input("Overwrite old data? (y/n): "))
                if overwrite == "y" or overwrite == "n":
                    break
        else:
            overwrite = "n"
    numExisting = len(existingMembers)
    tempwrite = tempfile.NamedTemporaryFile("w+t", newline = "", delete = False)
    with open("memberdata.csv", "r", newline = "") as fr, tempwrite:
        reader = csv.DictReader(fr)
        writer = csv.DictWriter(tempwrite, fieldnames = fieldnames)
        writer.writeheader()
        for row in reader:
            if overwrite == "y":
                for member in existingMembers:
                    if row["Mno"] == member["Mno"]:
                        writer.writerow(member)
                        existingMembers.remove(member)
                        break
                    elif row["First name"] == member["First name"] and row["MI"] == member["MI"] and row["Last name"] == member["Last name"] and row["DoB"] == member["DoB"]:
                        writer.writerow(member)
                        existingMembers.remove(member)
                        break
                else:
                    writer.writerow(row)
            else:
                writer.writerow(row)
        for member in acceptedMembers:
            writer.writerow(member)

    shutil.move(tempwrite.name, "memberdata.csv")
    print("{} new members added" .format(len(acceptedMembers)))
    if overwrite == "y":
        print("{} members overwritten" .format(numExisting))
    print("{} members with invalid attributes found" .format(len(invalidAttr)))
    # for member in invalidAttr:
    #     print(member["Mno"])

    print("{} members with missing attributes found" .format(len(missingAttr)))
    # for member in missingAttr:
    #     print(member["Mno"])
            # open("memberdate.csv", "r", newline = "") as oldData:

def searchMember():
    getMember(search = 1)
#
def bulkOperation():
    print("Please select bulk operation option:")
    print("[a] : Push renewal date")
    print("[b] : Change membership status")
    print("[c] : Delete members")
    while True:
        try:
            option = str(input("Enter [a] - [c] : "))
        except:
            print("Error, invalid input")
            continue
        if option in ["a", "b", "c"]:
            if option == "a":
                while True:
                    option = [option,0]
                    try:
                        option[1] = int(input("Enter number of months to push membership renewal dates: "))
                        break
                    except:
                        print("Enter an integer amount of months to push membership renewal dates")
            elif option == "b":
                option = [option,0]
                while True:
                    option[1] = str(input("Enter new status: "))
                    if option[1] in ["Basic", "Silver", "Gold", "Platinum", "None"]:
                        break
                    else:
                        print("Invalid status, enter (Basic, Silver, Gold, Platinum, None): ")
            else:
                option = [option,0]

            break
        else:
            print("Error, invalid input")
    print("Please select bulk operation target members:")
    print("Age: <min age*> < max age> : Members for a given age range")
    print("Member: <min period* in years in integer> <max period in years> : Members who have been members for more than a certain period")
    print("Status: <Status> : Members with certain membership status")
    while True:
        try:
            criteria = list()
            inputs = str(input("Enter member criteria: "))
            age = re.search("Age:?\s*(\d+)\s*(\d*)", inputs)
            if age:
                criteria.append("Age")
            period = re.search("Member:?\s*(\d+)\s*(\d*)", inputs)
            if period:
                criteria.append("Member")
            status = re.search("Status:?(?:\s+(Basic)|\s+(Platinum)|\s+(Gold)|\s+(Silver)|\s+(None))+", inputs)
            if status:
                criteria.append("Status")
            if len(criteria) == "0":
                print("Error, no valid criteria entered")
                continue
            else:
                break
        except:
            print("Error, invalid input")
            continue
    tempwrite = tempfile.NamedTemporaryFile("w+t", newline = "", delete = False)
    with open("memberdata.csv", "r", newline = "") as fr, tempwrite:
        fieldnames = ["Mno", "First name", "MI", "Last name", "DoB", "Address", "Status", "msd", "med", "rdate", "Phone", "Email", "Notes"]
        reader = csv.DictReader(fr)
        writer = csv.DictWriter(tempwrite, fieldnames = fieldnames)
        writer.writeheader()
        for row in reader:
            isTarget = 0
            if "Age" in criteria:
                dob = datetime.datetime.strptime(row["DoB"], "%B %d %Y")
                memAge = datetime.date.today().year - dob.year - ((datetime.datetime.today().month, datetime.datetime.today().day) < (dob.month, dob.day))
                if age.group(2):
                    if memAge > int(age.group(1)) and memAge < int(age.group(2)):
                        isTarget += 1
                else:
                    if memAge > int(age.group(1)):
                        isTarget += 1
            if "Member" in criteria:
                msd = datetime.datetime.strptime(row["msd"], "%B %d %Y")#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                accAge = datetime.date.today().year - msd.year - ((datetime.datetime.today().month, datetime.datetime.today().day) < (msd.month, msd.day))
                if period.group(2):
                    if accAge > int(period.group(1)) and accAge < int(period.group(2)):
                        isTarget += 1
                    else:
                        if accAge > int(period.group(1)):
                            isTarget += 1
            if "Status" in criteria:
                if row["Status"] in status.groups():
                    isTarget += 1
            if isTarget == len(criteria):
                if option[0] == "a":
                    rdate = datetime.datetime.strptime(row["rdate"], "%B %d %Y")
                    rdate.month = (rdate.month + option[1]) % 12
                    rdate.year = option[1] // 12
                    newMember = row
                    newMember["rdate"] = rdate.strftime("%B %d %Y")
                    writer.writerow(newMember)
                    continue
                elif option[0] == "b":
                    newMember = row
                    newMember["Status"] = option[1]
                    if option[1] == "None":
                        if newMember["med"] == "":
                            newMember["med"] = datetime.datetime.today().strftime("%B %d %Y")
                    else:
                        if newMember["med"] != "":
                            newMember["med"] = ""
                    writer.writerow(newMember)
                    continue
                elif option[0] == "c":
                    newMember = row
                    newMember["Status"] = "None"
                    if newMember["med"] == "":
                        newMember["med"] = datetime.datetime.today().strftime("%B %d %Y")
                    writer.writerow(newMember)
                    continue
            else:
                writer.writerow(row)



    shutil.move(tempwrite.name, "memberdata.csv")

def helpfn(option:str = ""):
    print("Please select option:")
    print("[a] : General information")
    print("[b] : Program operation option information")
    print("[c] : Member data file information")
    if option == "":
        try:
            option = str(input("Enter [a] - [c] : "))
        except:
            print("Error, invalid input")
    if option == "a":
        print("This program is designed to allow the user to manage a database of memberships.\n")
        print("This program also has the option to plot data on the members by running Manage_memebrs.py --graph [option]")
        print("The graphing function has the opton to graph members by status, age, or year\n")
        print("This program utilizes pynput, matplotlib, and numoy librarys outside of the standard library")
    elif option == "b":
        print("Option descriptions:")
        print("[a] : Add new member: Asks for member information in order to create a new member to ad to the system")
        print("[b] : Remove member: Allows user to search for a member to end their membership")
        print("[c] : Upgrade/Downgrade membership: Allows user to search for a member to change their status")
        print("[d] : Modify member data: Allows user to search for a member to change an attribute")
        print("[e] : Import members (csv or txt file): Allows user to import members from another file")
        print("[f] : Search for member: Allows user to search for a member")
        print("[g] : Bulk operation: Allows user to preform certain operations on multiple users")
    elif option == "c":
        print("Member data is stored in memberdata.csv")
        print("The first row of the file must be the csv dictionary header:")
        print("Mno,First name,MI,Last name,DoB,Address,Status,msd,med,rdate,Phone,Email,Notes")


def graphMembers(choice:str):
    if choice == "Status":
        x = ["None", "Basic", "Silver", "Gold", "Platinum"]
        y = [0, 0, 0, 0, 0]
        with open("memberdata.csv", "r", newline = "") as fr:
            reader = csv.DictReader(fr)
            for row in reader:
                if row["Status"] == "None":
                    y[0] += 1
                elif row["Status"] == "Basic":
                    y[1] += 1
                elif row["Status"] == "Silver":
                    y[2] += 1
                elif row["Status"] == "Gold":
                    y[3] += 1
                elif row["Status"] == "Platinum":
                    y[4] += 1
        plt.xlabel("Status")
        plt.ylabel("Number of members")
        plt.title("Number of members for each membership status")
        plt.bar(x,y)
        plt.show()
    elif choice == "Age":
        x = ["18-25", "25-35", "35-50", "50-65", ">65"]
        y = [0, 0, 0, 0, 0]
        with open("memberdata.csv", "r", newline = "") as fr:
            reader = csv.DictReader(fr)
            for row in reader:
                dob = datetime.datetime.strptime(row["DoB"], "%B %d %Y")
                age = datetime.date.today().year - dob.year - ((datetime.datetime.today().month, datetime.datetime.today().day) < (dob.month, dob.day))
                if age < 25:
                    y[0] += 1
                elif age < 35:
                    y[1] += 1
                elif age < 50:
                    y[2] += 1
                elif age < 65:
                    y[3] += 1
                else:
                    y[4] += 1
        plt.xlabel("Age Range")
        plt.ylabel("Number of members")
        plt.title("Number of members for each age range")
        plt.bar(x,y)
        plt.show()
    elif choice == "Year":
        xLabel = list()
        y_new = list()
        y_ended = list()
        for i in range(1981, 2020):
            xLabel.append(i)
            y_new.append(0)
            y_ended.append(0)
        x = np.arange(len(y_new))
        with open("memberdata.csv", "r", newline = "") as fr:
            reader = csv.DictReader(fr)
            for row in reader:
                msd = datetime.datetime.strptime(row["msd"], "%B %d %Y")
                if msd.year <= 2019 and msd.year >= 1981:
                    y_new[msd.year - 1981] += 1
                if row["med"] != "":
                    med = datetime.datetime.strptime(row["med"], "%B %d %Y")
                    if med.year <= 2019 and med.year >= 1981:
                        y_ended[med.year - 1981] += 1
        f = plt.figure()
        f.set_figwidth(15)
        f.set_figheight(6)
        plt.bar(x - .2, y_new, label = "Number of members who joined", width = .4)
        plt.bar(x + .2, y_ended, label = "Number of members who left", width = .4)
        plt.xlabel("Year")
        plt.ylabel("Number of members")
        plt.xticks(range(len(xLabel)), xLabel, rotation = 45)
        plt.title("Number of members who joined and left each year")
        plt.legend()
        plt.show()





def main():
    while True:
        print("Please select option:")
        print("[a] : Add new member")
        print("[b] : Remove member")
        print("[c] : Upgrade/Downgrade membership")
        print("[d] : Modify member data")
        print("[e] : Import members (csv or txt file)")
        print("[f] : Search for member")
        print("[g] : Bulk operation")
        print("[h] : Help")
        try:
            option = str(input("Enter [a] - [h] : "))
        except:
            print("Error, invalid input")
        if option == "a":
            addMember()
        elif option == "b":
            removeMember()
        elif option == "c":
            changeStatus()
        elif option == "d":
            modifyData()
        elif option == "e":
            importData()
        elif option == "f":
            searchMember()
        elif option == "g":
            bulkOperation()
        elif option == "h":
            helpfn()
            while True:
                try:
                    ret = str(input("Return to menu? (y/n): "))
                    if ret == "y":
                        break
                    elif ret == "n":
                        quit()
                    else:
                        print("Invalid input")
                except:
                    print("Error, invalid input")
            continue
        elif option == "":
            quit()
        else:
            helpfn("b")
            while True:
                try:
                    ret = str(input("Return to menu? (y/n): "))
                    if ret == "y":
                        break
                    elif ret == "n":
                        quit()
                    else:
                        print("Invalid input")
                except:
                    print("Error, invalid input")
            continue
        quit()

if __name__=="__main__":
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        # try:
        # listener.start()
        parser = argparse.ArgumentParser(prog = "Manage_members")
        parser.add_argument("--graph", choices = ["Status", "Age", "Year"], help = "Plots data from memberdata based on selected mode. Valid modes: [Status], [Age], [Year]")
        args = parser.parse_args()
        if args.graph:
            print(args.graph)
            graphMembers(args.graph)
            quit()
        main()
