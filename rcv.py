import gspread
import random
import plotly.plotly as py
from plotly import tools

# change for your account
tools.set_credentials_file(username='[INSERT_PLOTLY_USERNAME]', api_key='[INSERT_PLOTLY_API_KEY]')

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
    '#17becf'   # blue-teal
]

# Competition Architect
# SpreadSheetID = '1h8eHCD52o51jZj3ztTTAXoZ3R2fMyvF54B5L4jPgu0I'

# PR
# SpreadSheetID = '1fIjCCKSMa1u66K7e9_MiHkBCOLykDGEcfq-H9Ffx8aQ'

# Head Of Education
# SpreadSheetID = '1TtdnzRF5DXDmL_MaEW38Q3JpkTRd_MBMOB5FFD6M7Go'

# Head Of Research
#SpreadSheetID = '13pe1BzmSH1Bf-PAKnS8b-JlTy4eJR4Et3-LKZKcoQRU'

# President
SpreadSheetID = '1HaRjyPie3mmmXcZxpBwC6mxC2mBkzuNMmX4m-VR-5p0'

# Secretary
# SpreadSheetID = '1SQKh0swkhPvdYCl1fIzDK47rKC-gPBlaYKAOx_OBl5E'

# Treasurer
# SpreadSheetID = '1Tqban_9U50zGuj7PPDsrLjGapyaDMa512KRobLGN9lc'


OAuthClientSecretJSON = 'creds.json'
RosterFile = 'roster_file'

roster = set()

def fill_roster():
	with open('roster_file') as f:
		for line in f:
			roster.add(line.strip())


def print_round(round_num, tallies, titles):
	votes = {}
	print("======================================================")
	print("Round {}".format(round_num))
	print("======================================================")
	titles = titles[1:]
	for i in range(len(titles)):
		candidate_pre = titles[i]
		candidate_name = candidate_pre[candidate_pre.index('[')+1:-1]
		votes[candidate_name] = tallies[i]
		print("{} -> {} votes".format(candidate_name, tallies[i]))
	print ""
	return votes

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

def perform_elections(worksheet):
	vals = None
	titles = worksheet.row_values(1)
	titles = titles[1:]  # timestamps are useless
	num_candidates = len(titles[1:]) # dont include emails also
	i = 2
	vals = worksheet.row_values(2)[1:]  # again, timestamps bad
	ballots = []

	while(vals != []):
		ballot = {}
		email = vals[0]
		username = email[:email.index('@')] # remove emaily bits
		vals = vals[1:] # remove username
		if username not in roster:
			print("{} tried to vote but not in roster, now skipping...".format(username))
		else:
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

	vote_data = []

	for ballot in ballots:
		vote = get_top_candidate_in_play(ballot, candidates_removed)
		tallies[vote] += 1
	vote_data.append(print_round(round_num, tallies, titles))


	for round_num in range(1,num_candidates):
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

def get_candidate_labels(vote_data):
	candidates = []
	for round_num in range(len(vote_data)):
		round_data = vote_data[round_num]
		for name in round_data:
			if round_num == 0 or round_data[name] != 0:
				candidates.append(name+'-Round '+str(round_num))
	return candidates

def get_dropped_candidate(prev_round, curr_round):
	for candidate in prev_round:
		if prev_round[candidate] != 0 and curr_round[candidate] == 0:
			return candidate

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

def plot_data(vote_data):
	candidate_labels = get_candidate_labels(vote_data)
	colors = get_colors(candidate_labels)

	prev_round = vote_data[0]

	source = []
	target = []
	value = []

	for round_num in range(1, len(vote_data)):
		curr_round = vote_data[round_num]

		# get dropped candidate index
		dropped_candidate = get_dropped_candidate(prev_round, curr_round)
		dropped_candidate_label = dropped_candidate+'-Round '+str(round_num-1)
		dropped_candidate_index = candidate_labels.index(dropped_candidate_label)

		for candidate in curr_round:
			# carry values from previous round, if not dropped
			if curr_round[candidate] != 0:
				candidate_prev_round_label = candidate+'-Round '+str(round_num-1)
				candidate_prev_round_index = candidate_labels.index(candidate_prev_round_label)
				candidate_prev_round_val = prev_round[candidate]
				candidate_curr_round_label = candidate+'-Round '+str(round_num)
				candidate_curr_round_index = candidate_labels.index(candidate_curr_round_label)
				source.append(candidate_prev_round_index)
				target.append(candidate_curr_round_index)
				value.append(candidate_prev_round_val)

			# values being spread from dropped candidate
			moved_val = curr_round[candidate] - prev_round[candidate]
			if moved_val > 0:
				target_label = candidate+'-Round '+str(round_num)
				target_index = candidate_labels.index(target_label)
				source.append(dropped_candidate_index)
				target.append(target_index)
				value.append(moved_val)


		# next round
		prev_round = vote_data[round_num]

	data = dict(
	    type='sankey',
	    node = dict(
	      pad = 30,
	      thickness = 20,
	      line = dict(
	        color = "black",
	        width = 0.5
	      ),
	      label = candidate_labels,
	      color = colors
	    ),
	    link = dict(
	      source = source,
	      target = target,
	      value = value
	  ))

	layout =  dict(
	    title = "RITSEC Elections",
	    font = dict(
	      size = 16
	    )
	)

	fig = dict(data=[data], layout=layout)
	print("View Plot at {}".format(py.plot(fig, validate=False)))

if __name__ == "__main__":
	fill_roster()
	worksheet = create_worksheet()
	vote_data = perform_elections(worksheet)
	plot_data(vote_data)
