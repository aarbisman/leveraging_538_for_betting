import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import re
import datetime

## This function adjusts the times for our webscraper
def time_adj(time_str, timedelta):
    
    time = datetime.datetime.strptime(time_str, '%I:%M%p').time()
    
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    
    return_time = end.time().strftime('%I:%M%p')
    return return_time



## Coneect to the url
URL = "https://sportsbook.draftkings.com/leagues/baseball/88670847?category=game-lines&subcategory=game"
page = requests.get(URL)

#Store the contents of the website under doc
doc = lh.fromstring(page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

rows = [row.text_content() for row in tr_elements]

## We record the table headers------------POSSIBLE DELETE
# today_index = rows.index('Today RUN LINETOTALMONEYLINE')
# tomorrow_index = rows.index('Tomorrow RUN LINETOTALMONEYLINE')

## We remove the header for the "tomorrow" games, since the web-scrapers time zone is 4 hours ahead of the 538 one
rows.remove("Tomorrow RUN LINETOTALMONEYLINE")


## We initialize our max time variabe with 00:00 for our max_time finder
max_time = datetime.datetime.strptime("20/01/2020" ,"%d/%m/%Y").time()
rows_for_today = []

## Since the draft king rows are all in ascending order, we keep looping through the list of rows until we get a game time
## that is not greater than/equal to our max time, once that happens, we are done with today's games and the loop is broken
for row in rows[1:57]:
    
    ## This current if statement excludes games that are ongoing
    if re.search("[0-9]{1,2}\:[0-9]{1,2}[A-Z]{2}", row) is not None:
        time_stamp = re.search("[0-9]{1,2}\:[0-9]{1,2}[A-Z]{2}", row).group()
        time_stamp_adj = time_adj(time_stamp, datetime.timedelta(hours = -4))
        time = datetime.datetime.strptime(time_stamp_adj, '%I:%M%p').time()
    
        if time >= max_time:
        
            max_time = time
        
            rows_for_today.append(row)
        
        else:
            break
            
## We loop through the rows_for today to extract game information
game_moneylines = []

for i in range(0,len(rows_for_today),2):
    
    away_team_row = rows_for_today[i]
    home_team_row = rows_for_today[i + 1] 
    
    ## We get todays date
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    
    ## This regex method is a little clunky, but it works with one word and two word teams given Draft kings formatting
    ## We get the away teams name
    away_team_list = re.findall(" [A-Z][a-z]+", away_team_row)
    
    if away_team_list[0] in [" Red", " White", " Blue"]:
        away_team = ''.join(away_team_list[0:2])[1:]
    else:
        away_team = ''.join(away_team_list[0:1])[1:]
    
    ## and the home tams name
    home_team_list = re.findall(" [A-Z][a-z]+", home_team_row)
    
    if home_team_list[0] in [" Red", " White", " Blue"]:
        home_team = ''.join(home_team_list[0:2])[1:]
    else:
        home_team = ''.join(home_team_list[0:1])[1:]
    
    ## We get the away teams moneyline
    away_team_moneyline = re.findall("((\+|\-)[0-9]+)", away_team_row)[-1][0]
    
    ## We get the home teams moneyline
    home_team_moneyline = re.findall("((\+|\-)[0-9]+)", home_team_row)[-1][0]
    
    moneyline_row = [date, away_team, home_team, away_team_moneyline, home_team_moneyline]
    

    game_moneylines.append(moneyline_row)

game_moneylines_df = pd.DataFrame(game_moneylines, columns=['game_date', 'away_team', 'home_team','away_ml_dk','home_ml_dk'])

## get the todays date for the name of the output file
today_dt = datetime.date.today()
today_str = today_dt.strftime("%m_%d_%Y")
file_name = "dk_scrape_output_" + today_str + ".csv"

## and write to csv
output_dir = "C:/Users/arbis/Projects/nate_silver_gets_me_money/data_dump/"
output_str = output_dir + file_name
game_moneylines_df.to_csv(output_str, index=False)