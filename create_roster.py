#!/usr/bin/env python3

import csv
from xml.etree.ElementInclude import include

# create three documents: signins.txt, members.txt, and presenters.txt
# signins.txt needs to have all the emails from the weekly sign in form and the IP/IG sign ins
# presenters.txt needs to have all the emails from all the presenters for this year
# members.txt will the output file and contain a list of every active member of RITSEC for this year

f2 = open("members.txt", "w")
f3 = open("presenters.txt", "r")
fml = open("igipmess.txt")

fields = []
rows = []
presenters = []
emails = {}
dates = {}
valid_names = {}
invalid_names = []

with open('signin.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    fields = next(reader)
    for row in reader:
        rows.append(row)

for row in rows:
    date = row[0].split()[0]
    if date in dates:
        dates[date] = dates[date] + 1
    else:
        dates[date] = 1

for row in rows:
    date = row[0].split()[0]
    email = row[2]
    if dates[date] > 5:
        email = email.strip().lower().split('@')[0]
        if email in emails:
            emails[email] = emails[email] + 1
        else:
            emails[email] = 1
    else:
        continue
   

for email in emails:
    if emails[email] >= 3:
        f2.write(email + '\n')

for email in f3:
    email = email.strip().lower().split('@')[0]
    if email not in presenters:
        presenters.append(email)
for i in presenters:
    f2.write(i + '\n')