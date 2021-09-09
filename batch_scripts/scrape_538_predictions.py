## Web scraping the upcoming game predicitons from 538 -- Alex Arbisman
## Imports
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import re
import datetime

## Coneect to the url
URL = "https://projects.fivethirtyeight.com/2021-mlb-predictions/games/"
page = requests.get(URL)

#Store the contents of the website under doc
doc = lh.fromstring(page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

## There are two tables on 538's website that use the same header, we parse through the table rows to get the header indecies
upcoming_list_done = False
future_list_done = False

rows = [row.text_content() for row in tr_elements]
header_str = "DateTeamStarting pitcherTeam ratingStarting pitcher adj.Travel, rest & home field adj.Pregame team ratingWin prob.Chance of winningScore"

## usually, it looks like 0-200 are the first table, and 201-end is the 2nd table, ymmv
indexes = [i for i,row in enumerate(rows) if row == header_str]

upcoming_games_header = rows[indexes[0]]
upcoming_games_rows = rows[indexes[0] + 1:indexes[1]]

previous_games_header = rows[indexes[1]]
previous_games_rows = rows[indexes[1] + 1:]

game_predictions = []

for i in range(0,len(upcoming_games_rows),2):
    
    ## We seperate the two tables
    row_w_game_info = upcoming_games_rows[i]
    row_w_team_only = upcoming_games_rows[i + 1]
        
    ## We get the team names and the date
    date = re.search("[0-9]{1,2}\/[0-9]{1,2}", row_w_game_info).group()
    month, day = date.split("/")
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    date = "2021-" + month + "-" + day        
   
    away_team = re.search("[A-Z]{3}", row_w_game_info).group()
    home_team = re.search("[A-Z]{3}", row_w_team_only).group()
    
    ## This is a combination of team score (4 digit) and percentage (1-2 digit plus percent symbol)
    away_pct_538_str = re.search("[0-9]{5,6}%", row_w_game_info).group()
    if len(away_pct_538_str) == 7:
        away_pct_538 = away_pct_538_str[-3:]
    elif len(away_pct_538_str) == 6:
        away_pct_538 = away_pct_538_str[-2:]  
        
    home_pct_538_str = re.search("[0-9]{5,6}%", row_w_team_only).group()
    if len(home_pct_538_str) == 7:
        home_pct_538 = home_pct_538_str[-3:]
    elif len(home_pct_538_str) == 6:
        home_pct_538 = home_pct_538_str[-2:]

    ## build a prediction row list and append it to a list of lists
    prediction_row = [date,away_team,home_team,away_pct_538,home_pct_538]
    game_predictions.append(prediction_row)

## We build a dataframe from our list of lists
game_predictions_df = pd.DataFrame(game_predictions, columns=['game_date', 'away_team', 'home_team','away_pct_538','home_pct_538'])

## get the todays date for the name of the output file
today_dt = datetime.date.today()
today_str = today_dt.strftime("%m_%d_%Y")
file_name = "538_scrape_output_" + today_str + ".csv"

## and write to csv
output_dir = "C:/Users/arbis/Projects/nate_silver_gets_me_money/data_dump/"
output_str = output_dir + file_name
game_predictions_df.to_csv(output_str, index=False)