import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Not Sure a better way to Map Human Readable to Code
# Also, zero index ;)
ChoiceMap = {
	u"First Choice": 0,
	u"Second Choice": 1,
	u"Third Choice": 2,
	u"Fourth Choice": 3,
	u"Fifth Choice": 4,
	u"Sixth Choice": 5,
	u"Seventh Choice": 6,
	u"Eighth Choice": 7,
	u"Ninth Choice": 8,
	u"Tenth Choice": 9
}

SpreadSheetID = '1qOz6HUTDW1JCi4Qhxq64rUrHRTUIb5cpmci2_ciED4k'
OAuthClientSecretJSON = '../creds.json'






def print_round(round_num, tallies, titles):
	print("======================================================")
	print("Round {}".format(round_num))
	print("======================================================")
	for i in range(len(titles)):
		candidate_pre = titles[i]
		candidate_name = candidate_pre[candidate_pre.index('[')+1:-1]
		print("{} -> {} votes".format(candidate_name, tallies[i]))
	print ""

def get_lowest_candidate(tallies, candidates_removed):
	lowest = 0
	for t in tallies:
		if tallies[t] < tallies[lowest] and t not in candidates_removed:
			lowest = t
	return lowest

def get_top_candidate_in_play(ballot, candidates_removed):
	# we will do it th dumb way... :P
	for position in range(len(ballot)):
		for candidate in ballot:
			if (ballot[candidate] == position) and (candidate not in candidates_removed):
				return candidate

def create_worksheet():
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(OAuthClientSecretJSON, scope)
	client = gspread.authorize(creds)

	# be sure to share the results sheet with the client_email in cred.json
	return client.open_by_key(SpreadSheetID).sheet1



if __name__ == "__main__":
	worksheet = create_worksheet()

	vals = None
	titles = worksheet.row_values(1)
	titles = titles[1:]  # timestamps are useless
	num_candidates = len(titles)
	i = 2
	vals = worksheet.row_values(2)[1:]  # again, timestamps bad
	ballots = []

	while(vals != []):
		ballot = {}
		for candidate in range(num_candidates):
			ballot[candidate] = ChoiceMap[vals[candidate]]
		ballots.append(ballot)
		i+=1
		vals = worksheet.row_values(i)[1:]


	# Do first round manually
	tallies = {}
	for candidate in range(num_candidates):
		tallies[candidate] = 0
	round_num  = 0
	candidates_removed = set()


	for ballot in ballots:
		vote = get_top_candidate_in_play(ballot, candidates_removed)
		tallies[vote] += 1
	print_round(round_num, tallies, titles)



	for round_num in range(1,num_candidates):
		lowest = get_lowest_candidate(tallies, candidates_removed)
		candidates_removed.add(lowest)
		tallies = {}
		for candidate in range(num_candidates):
			tallies[candidate] = 0


		for ballot in ballots:
			vote = get_top_candidate_in_play(ballot, candidates_removed)
			tallies[vote] += 1
		print_round(round_num, tallies, titles)




