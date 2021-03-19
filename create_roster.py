#!/usr/bin/env python3

# create three documents: signins.txt, members.txt, and presenters.txt
# signins.txt needs to have all the emails from the weekly sign in form and the IP/IG sign ins
# presenters.txt needs to have all the emails from all the presenters for this year
# members.txt will the output file and contain a list of every active member of RITSEC for this year

f = open("signin.txt", "r")
f2 = open("members.txt", "w")
f3 = open("presenters.txt", "r")
d = dict()
presenters = []

for email in f:
    email = email.strip().lower().split(',')[0].split('@')[0]
    if email in d:
        d[email] = d[email] + 1
    else:
        d[email] = 1
for email in list(d.keys()):
    if d[email] >= 3:
        f2.write(email + '\n')

for email in f3:
    email = email.strip().lower().split('@')[0]
    if email not in presenters:
        presenters.append(email)
for i in presenters:
    f2.write(i + '\n')