# import gspread
import random
# import chart_studio.plotly as py
# from chart_studio import tools
from datetime import time
import csv

# Plotly Credentials
# tools.set_credentials_file(username='INSERT_YOURS_HERE', api_key='INSERT_YOURS_HERE')

# updated oauth
# from google.oauth2.service_account import Credentials


# Not Sure a better way to Map Human Readable to Code
# Also, zero index ;)
ChoiceMap = {
    u"1st": 0,
    u"2nd": 1,
    u"3rd": 2,
    u"4th": 3,
    u"5th": 4,
    u"6th": 5,
    u"7th": 6,
    u"8th": 7,
    u"9th": 8,
    u"10th": 9
}

PlotColors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'  # blue-teal
]

# ISTS Competition Architect
# SpreadSheetID = '1Rp4YhSKWshF5DQVMInJlLXRhXBFts6ntky0aoz_mieE'

# Test Spreadsheet
# SpreadSheetID = '1zcplNSc7Z9k13Y5en5UqKty_IuGku8GDOCt080ORF3E'

# OAuthClientSecretJSON = 'creds.json'
RosterFile = 'members.txt'

roster = set()


# Roster is a set that contains the usernames of all eligible voters
# See the ReadMe for help on creating members.txt
def fill_roster():
    with open('members.txt') as f:
        for line in f:
            roster.add(line.strip())


# Prints the round in a nice format
# returns a dictionary with key:value pairs of name:votes
def print_round(round_num, tallies, titles):
    votes = {}
    print("======================================================")
    print("Round {}".format(round_num))
    print("======================================================")
    titles = titles[1:]
    for i in range(len(titles)):
        candidate_pre = titles[i]
        candidate_name = candidate_pre[candidate_pre.index('[') + 1:-1]
        votes[candidate_name] = tallies[i]
        print("{} -> {} votes".format(candidate_name, tallies[i]))
    print("")
    return votes


# Eliminates the candidate with the lowest votes in the round
def get_lowest_candidate(tallies, candidates_removed):
    lowest = [0]
    for t in tallies:
        if tallies[t] < tallies[lowest[0]] and t not in candidates_removed:
            lowest = [t]
        if tallies[t] == tallies[lowest[0]] and t not in candidates_removed:
            lowest.append(t)
    # in the event of a tie for lowest. It is often just chosen at random
    # Source: https://politics.stackexchange.com/q/9749# if ties choose random candidate
    return random.choice(lowest)


# Goes through the ballot, selecting the candidate that will be used for the round
# Returns the name of the candidate
def get_top_candidate_in_play(ballot, candidates_removed):
    # we will do it the dumb way... :P
    for position in range(len(ballot)):
        for candidate in ballot:
            if (ballot[candidate] == position) and (candidate not in candidates_removed):
                return candidate


# Uses the credentials to get the worksheet that contains the votes
# Returns the spreadsheet
# def create_worksheet():
#     # use creds to create a client to interact with the Google Drive API
#     scopes = [
#         'https://www.googleapis.com/auth/spreadsheets',
#         'https://www.googleapis.com/auth/drive'
#     ]
#     credentials = Credentials.from_service_account_file(OAuthClientSecretJSON, scopes=scopes)
#     client = gspread.authorize(credentials)

#     # be sure to share the results sheet with the client_email in cred.json
#     return client.open_by_key(SpreadSheetID).sheet1


# Algorithm for a Ranked-Choice-Vote Election
# Takes the worksheet with the votes as a parameter
# Returns a list of the vote_data
def perform_elections(worksheet):
    reader = csv.reader(worksheet, delimiter=',', quotechar='|')
    titles = next(reader)
    titles = titles[1:]  # timestamps are useless
    num_candidates = len(titles[1:])  # don't include emails also

    ballots = []

    for row in reader:
        try:
            # vals = worksheet.row_values(i)[1:]
            vals = row[1:]
            # time_stamp = worksheet.row_values(i)[0]
        except IndexError:
            break

        # #Time Stamp Verification Set Up
        # time_stamp = time_stamp.split()[1]
        # # split on ":"
        # stamp_hour = time_stamp.split(":")[0]
        # stamp_min = time_stamp.split(":")[1]
        # stamp_sec = time_stamp.split(":")[2]

        # create datatime objects for comparisons
        # open_stamp = time(OpenVoteHour, OpenVoteMin, 0)
        # close_stamp = time(CloseVoteHour, CloseVoteMin, 0)
        # vote_stamp = time(int(stamp_hour), int(stamp_min), int(stamp_sec))

        ballot = {}
        email = vals[0]
        username = email[:email.index('@')]  # remove emaily bits
        vals = vals[1:]  # remove username
        if username not in roster:
            # checks for attendance
            print("{} tried to vote but not eligible, now skipping...".format(username))
        # elif open_stamp > vote_stamp:
        #     # checks for voting before poll was opened
        #     print("{} tried to vote, but cast their vote before the poll was open, now skipping...".format(username))
        # elif vote_stamp > close_stamp:
        #     # checks for voting after poll was closed
        #     print("{} tried to vote, but cast their vote after the poll was closed, now skipping...".format(username))
        else:
            # vote and voter passes all checks, let them vote
            for candidate in range(num_candidates):
                ballot[candidate] = ChoiceMap[vals[candidate]]
            ballots.append(ballot)

    # Do first round manually
    tallies = {}
    for candidate in range(num_candidates):
        tallies[candidate] = 0
    round_num = 0
    candidates_removed = set()

    vote_data = []

    for ballot in ballots:
        vote = get_top_candidate_in_play(ballot, candidates_removed)
        tallies[vote] += 1
    vote_data.append(print_round(round_num, tallies, titles))

    for round_num in range(1, num_candidates):
        lowest = get_lowest_candidate(tallies, candidates_removed)
        candidates_removed.add(lowest)
        tallies = {}
        for candidate in range(num_candidates):
            tallies[candidate] = 0

        for ballot in ballots:
            vote = get_top_candidate_in_play(ballot, candidates_removed)
            tallies[vote] += 1
        vote_data.append(print_round(round_num, tallies, titles))
    return vote_data


# Helps plotly
def get_candidate_labels(vote_data):
    candidates = []
    for round_num in range(len(vote_data)):
        round_data = vote_data[round_num]
        for name in round_data:
            if round_num == 0 or round_data[name] != 0:
                candidates.append(name + '-Round ' + str(round_num))
    return candidates


# Helps plotly
def get_dropped_candidate(prev_round, curr_round):
    for candidate in prev_round:
        if prev_round[candidate] != 0 and curr_round[candidate] == 0:
            return candidate


# Helps plotly
def get_colors(candidate_labels):
    color_map = {}
    colors = []
    for candidate_label in candidate_labels:
        real_candidate = candidate_label[:candidate_label.index('-')]
        if real_candidate not in color_map:
            color_map[real_candidate] = random.choice(PlotColors)
            PlotColors.remove(color_map[real_candidate])
        colors.append(color_map[real_candidate])
    return colors


# # Does the plotly
# def plot_data(vote_data):
#     candidate_labels = get_candidate_labels(vote_data)
#     colors = get_colors(candidate_labels)

#     prev_round = vote_data[0]

#     source = []
#     target = []
#     value = []

#     for round_num in range(1, len(vote_data)):
#         curr_round = vote_data[round_num]

#         # get dropped candidate index
#         dropped_candidate = get_dropped_candidate(prev_round, curr_round)
#         dropped_candidate_label = dropped_candidate + '-Round ' + str(round_num - 1)
#         dropped_candidate_index = candidate_labels.index(dropped_candidate_label)

#         for candidate in curr_round:
#             # carry values from previous round, if not dropped
#             if curr_round[candidate] != 0:
#                 candidate_prev_round_label = candidate + '-Round ' + str(round_num - 1)
#                 candidate_prev_round_index = candidate_labels.index(candidate_prev_round_label)
#                 candidate_prev_round_val = prev_round[candidate]
#                 candidate_curr_round_label = candidate + '-Round ' + str(round_num)
#                 candidate_curr_round_index = candidate_labels.index(candidate_curr_round_label)
#                 source.append(candidate_prev_round_index)
#                 target.append(candidate_curr_round_index)
#                 value.append(candidate_prev_round_val)

#             # values being spread from dropped candidate
#             moved_val = curr_round[candidate] - prev_round[candidate]
#             if moved_val > 0:
#                 target_label = candidate + '-Round ' + str(round_num)
#                 target_index = candidate_labels.index(target_label)
#                 source.append(dropped_candidate_index)
#                 target.append(target_index)
#                 value.append(moved_val)

#         # next round
#         prev_round = vote_data[round_num]

#     data = dict(
#         type='sankey',
#         node=dict(
#             pad=30,
#             thickness=20,
#             line=dict(
#                 color="black",
#                 width=0.5
#             ),
#             label=candidate_labels,
#             color=colors
#         ),
#         link=dict(
#             source=source,
#             target=target,
#             value=value
#         ))

#     layout = dict(
#         title="RITSEC Elections",
#         font=dict(
#             size=16
#         )
#     )

#     fig = dict(data=[data], layout=layout)
#     print("View Plot at {}".format(py.plot(fig, validate=False)))


if __name__ == "__main__":
    fill_roster()
    worksheet = open("results.csv", "r")
    vote_data = perform_elections(worksheet)
    # plot_data(vote_data)
