import sqlite3
from sqlite3 import Error
import pandas as pd

def get_dicts():
    name_to_abr = {"Diamondbacks":"ARI",\
               "Braves":"ATL",\
               "Orioles":"BAL",\
               "Red Sox":"BOS",
               "Cubs":"CHC",\
               "White Sox":"CHW",
               "Reds":"CIN",\
               "Indians":"CLE",
               "Rockies":"COL",\
               "Tigers":"DET",
               "Marlins":"MIA",\
               "Astros":"HOU",
               "Royals":"KCR",\
               "Angels":"LAA",
               "Dodgers":"LAD",\
               "Brewers":"MIL",    
               "Twins":"MIN",    
               "Mets":"NYM",\
               "Yankees":"NYY",\
               "Athletics":"OAK",\
               "Phillies":"PHI",\
               "Pirates":"PIT",\
               "Padres":"SDP",\
               "Giants":"SFG",\
               "Mariners":"SEA",\
               "Cardinals":"STL",\
               "Rays":"TBR",\
               "Rangers":"TEX",\
               "Blue Jays":"TOR",\
               "Nationals":"WSH"}
    
    abr_to_id = {
    "ARI":1,\
    "ATL":2,\
    "BAL":3,\
    "BOS":4,\
    "CHC":5,\
    "CHW":6,\
    "CIN":7,\
    "CLE":8,\
    "COL":9,\
    "DET":10,\
    "MIA":11,\
    "HOU":12,\
    "KCR":13,\
    "LAA":14,\
    "LAD":15,\
    "MIL":16,\
    "MIN":17,\
    "NYM":18,\
    "NYY":19,\
    "OAK":20,\
    "PHI":21,\
    "PIT":22,\
    "SDP":23,\
    "SFG":24,\
    "SEA":25,\
    "STL":26,\
    "TBR":27,\
    "TEX":28,\
    "TOR":29,\
    "WSH":30}
    
    return name_to_abr, abr_to_id

def transform_dk(df):
    
    ## Get our data dictionaries
    from data_dicts import get_dicts

    name_to_abr, abr_to_id = get_dicts()
        
    df_abr  = df.replace({"away_team": name_to_abr, "home_team": name_to_abr})

    df_id = df_abr.replace({"away_team": abr_to_id, "home_team": abr_to_id})
    
    return df_id

def transform_538(df):
    
    ## Get our data dictionaries
    from data_dicts import get_dicts
    name_to_abr, abr_to_id = get_dicts()
    
    df_id = df.replace({"away_team": abr_to_id, "home_team": abr_to_id})
    
    df_id["away_pct_538"] = df_id["away_pct_538"].apply(lambda x: int(x[:-1])/100)
    df_id["home_pct_538"] = df_id["home_pct_538"].apply(lambda x: int(x[:-1])/100)

    return df_id  

def etl_dk(file_dk, conn):
    
    ## Load into a dataframe
    df_dk = pd.read_csv(file_dk)
    
    ## Transform the values to the proper dataset (team name into ids)
    df_dk = transform_dk(df_dk)
    
    ## Drop the duplicates
    to_add_dk = df_dk.drop_duplicates(subset=["game_date", "away_team", "home_team"], keep='last')
    
    cur = conn.cursor()
    for index, row in to_add_dk.iterrows():
    
        ## We create our insert/replace query 
        values_to_add = "('" + row.game_date + "', " + str(row.away_team) + ", " + str(row.home_team) + ", " + str(row.away_ml_dk) + ", " + str(row.home_ml_dk) + ")"
        insert_query = "INSERT or REPLACE INTO moneylines_dk (game_date, away_team, home_team, away_ml_dk, home_ml_dk) VALUES " + values_to_add
        
        ## and insert/replace the row into our database
        cur.execute(insert_query)
        conn.commit()
    
    cur.close()
    
    
    
def etl_538(file_538, conn):
    
    ## Load into a dataframe
    df_538 = pd.read_csv(file_538)
    
    ## Transform the values to the proper dataset (team name into ids)
    df_538 = transform_538(df_538)

    ## Drop the duplicates
    to_add_538 = df_538.drop_duplicates(subset=["game_date", "away_team", "home_team"], keep='last')
    
    cur = conn.cursor()
    for index, row in to_add_538.iterrows():
    
        ## We create our insert/replace query 
        values_to_add = "('" + row.game_date + "', " + str(row.away_team) + ", " + str(row.home_team) + ", " +  str(row.away_pct_538) + ", " + str(row.home_pct_538) + ")"
        insert_query = "INSERT or REPLACE INTO predictions_538 (game_date, away_team, home_team, away_pct_538, home_pct_538) VALUES " + values_to_add
        
                
        ## and insert/replace the row into our database        
        cur.execute(insert_query)
        
    cur.close()







