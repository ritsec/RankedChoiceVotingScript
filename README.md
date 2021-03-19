# RankedChoiceVotingScript
Using Google Sheets API to compute the winner of a Ranked Choice Voting Election, then makes a Sankey Chart to show the calculations.

## RCV.py Setup
### Environmental Variables
#### Plotly
Plotly is used to make the output look nice and fancy. Make an an account and get
the `INSERT_PLOTLY_USERNAME` and `INSERT_PLOTLY_API_KEY` values from `https://plot.ly/settings/api`.

#### SpreadSheetID
SpreadSheetID can be found by looking at the URL for the spreadsheet and finding: d/`<SpreadSheetID>`/edit


#### OAuthClientSecretJSON
This is generated for you by google :) just log in at `https://console.developers.google.com/apis/credentials` and set up a project, and add a service account with permissions and download the json file.
More info can be found here: `https://gspread.readthedocs.io/en/latest/oauth2.html`

Copy the JSON File into creds.json.

## Create_Roster.py Set Up
### Required Data
All of the emails from the sign in forms, including weekly and IP/IG sign ins, need to get copied into the signin.txt form.
The Head of Research should be keeping a list of presenters and their emails. Copy those emails into presenters.txt.

### Members.txt
Make sure that Members.txt is empty before running Create_Roster.py

##  Usage
Set up the google service account, share the spreadsheet with the account.

Run create_roster.py, then run rcv.py.



## Output
The script will print out the results of each round.
If plotly is fixed, it will also create a pretty graph and output a url for where the graph is located
