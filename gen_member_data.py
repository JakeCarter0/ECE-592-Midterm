"""
Created on June 8 2022

@author: Jake Carter
PiE Midterm file 1:
Includes code for generating random members for use by Manage_members.py


"""



import sys
import argparse
import csv
import random
import datetime
import os
# try:
#     import names
# except:
#     print("Warning: [names] library not installed, install with 'pip install names'")
#     sys.exit(-1)
try:
    import faker
except:
    print("Warning: [faker] library not installed, install with 'pip install faker'")
    sys.exit(-1)

parser = argparse.ArgumentParser(prog = "gen_member_data")
parser.add_argument("-no", type = int, default = 1000, help = "<NO> number of random members to be generated in file with <FNAME>")
parser.add_argument("-fname", type = str, default = "memberdata.csv", help = "The name of the generated file. Defaults to memberdata.csv")
args = parser.parse_args()

fieldnames = ["Mno", "First name", "MI", "Last name", "DoB", "Address", "Status", "msd", "med", "rdate", "Phone", "Email", "Notes"]
# Membership number* (Mno^): 6 digit number
memNoSet = set()
while len(memNoSet) < args.no:
    # memNoSet.add(random.randint(0, 999999))
    memNoSet.add(len(memNoSet))
memNoList = list(memNoSet)
random.shuffle(memNoList)

phoneNoSet = set()
while len(phoneNoSet) < args.no:
    phoneNoSet.add(random.randint(0, 9999999999))
phoneNoList = list(phoneNoSet)
random.shuffle(phoneNoList)

# Name: First name^*, middle name (MI^), Last name^*
# Date of birth*(DoB^): Date with format <Month DD Year> e.g. June 15 1996
# Address^: String
# Status^*: {Basic, Silver, Gold, Platinum, None}
# Membership start date* (msd^):
# Membership end date (med^)
# Renewal date* (rdate^):
# Phone^*:  10 digit number with format (##########)
# Email^: String
# Notes^:

l = list()
fake = faker.Faker()
namelist = set()
for i in range(0, args.no):
    l.append(dict())
    l[i]["Mno"] = memNoList[i]
    l[i]["Phone"] = phoneNoList[i]
    l[i]["Address"] = fake.address().replace("\n", ", ")
    l[i]["Email"] = fake.email()
    l[i]["Notes"] = fake.text()
    while True:
        l[i]["First name"] = fake.first_name()
        l[i]["MI"] = fake.first_name()
        l[i]["Last name"] = fake.last_name()
        DoB = fake.date_between(start_date = "-62y")
        msd = fake.date_between(start_date = DoB)
        try:
            DoB = DoB.replace(year = (DoB.year - 18))
        except:
            DoB = DoB.replace(day = 28, year = (DoB.year - 18))
        checkUnique = l[i]["First name"] + l[i]["MI"] + l[i]["Last name"] + str(DoB)
        if checkUnique not in namelist:
            namelist.add(checkUnique)
            break
    endDate = fake.date_between(start_date = msd,end_date = "+5y")
    if endDate < datetime.date.today():
        l[i]["med"] = endDate.strftime("%B %d %Y")
        l[i]["rdate"] = fake.date_between(start_date = datetime.date.today(), end_date = "+5y").strftime("%B %d %Y")
        l[i]["Status"] = "None"
    else:
        l[i]["rdate"] = endDate.strftime("%B %d %Y")
        l[i]["Status"] = random.choice(("Basic", "Silver", "Gold", "Platinum"))
    l[i]["DoB"] = DoB.strftime("%B %d %Y")
    l[i]["msd"] = msd.strftime("%B %d %Y")
if os.path.exists(args.fname):
  os.remove(args.fname)
with open(args.fname, "w", newline = "") as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(0, len(l)):
        writer.writerow(l[i])
print("{0} member file created with {1} entries." .format(args.fname, args.no))
