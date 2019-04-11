# RankedChoiceVotingScript
Using Google Sheets API to compute the winner of a Ranked Choice Voting Election, then makes a Sankey Chart to show the calculations.

## Setup
Change the two variables at the top of the script (`SpreadSheetID` and `OAuthClientSecretJSON`) these are crucial for the script to get the correct spreadsheet and permissions respectively. Also the `INSERT_PLOTLY_USERNAME` and `INSERT_PLOTLY_API_KEY` values are generated from `https://plot.ly/settings/api`.

### OAuthClientSecretJSON
This is generated for you by google :) just log in at `https://console.developers.google.com/apis/credentials` and set up a project with permissions and download the json file.

## Output
The script will output a url for where the graph is located. A Sample output can be seen below.
![ranked_voting_photo](https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/56696923_397162014448647_6961399597423919104_o.jpg?_nc_cat=109&_nc_ht=scontent-lga3-1.xx&oh=327c27bc2129dc54a62be5111d6ca812&oe=5D482A93)
