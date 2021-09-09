## Imports
import pandas as pd
import sqlite3
from sqlite3 import Error


## Connect to our database
database = r"C:\Users\arbis\Projects\nate_silver_gets_me_money\dk_538_games.db" 
con_db = sqlite3.connect(database)


## get a query that gets the game date, full names of each team, the draftkings moneyline, and the 538 percentages
select_query = "SELECT moneylines_dk.game_date , away_team.team_name as 'away', home_team.team_name as 'home'\
,moneylines_dk.away_ml_dk,moneylines_dk.home_ml_dk, predictions_538.away_pct_538 , predictions_538.home_pct_538 \
FROM moneylines_dk \
INNER JOIN team away_team ON (moneylines_dk.away_team = away_team.team_id) \
INNER JOIN team home_team ON (moneylines_dk.home_team = home_team.team_id) \
INNER JOIN predictions_538 ON (moneylines_dk.game_date = predictions_538.game_date AND \
moneylines_dk.away_team = predictions_538.away_team AND moneylines_dk.home_team = predictions_538.home_team)\
;"

## We save the query results to a dataframe and close the connection
rows_to_add = pd.read_sql_query(select_query, con_db)
con_db.close()


## We connect to our data warehouse
data_warehouse = r"C:\Users\arbis\Projects\nate_silver_gets_me_money\dk_538_games_dw.db" 
con_dw = sqlite3. connect(data_warehouse)
cur_dw = con_dw.cursor()

## for every row in our created dataframe:
for index, row in rows_to_add.iterrows():
    
    ## We create our insert/replace query     
    values_to_add = "('" + row.game_date + "', '" + str(row.away) + "', '" + str(row.home) + "', " + str(row.away_pct_538) + ", " + str(row.home_pct_538) + ", " + str(row.away_ml_dk) + ", " + str(row.home_ml_dk) + ");"
    insert_query = "INSERT or REPLACE INTO game_dw (game_date, away_team, home_team, away_pct_538, home_pct_538, away_moneyline_dk, home_moneyline_dk) VALUES " + values_to_add
        
    ## and insert/replace the row into our database        
    cur_dw.execute(insert_query)
    con_dw.commit()
        
cur_dw.close()
con_dw.close()