import os
import sys
import sqlite3
sys.path.insert(0, 'C:/Users/arbis/Projects/nate_silver_gets_me_money/helpers')

from etl_functions import etl_dk, etl_538

database = r"C:\Users\arbis\Projects\nate_silver_gets_me_money\dk_538_games.db" 
conn = None
try:
    conn = sqlite3.connect(database)
except Error as e:
    print(e)

data_dir = 'C:/Users/arbis/Projects/nate_silver_gets_me_money/' + 'data_dump/'

files = os.listdir(data_dir)

for f in files:
    
    if f[:3] == "538":
        file_name = data_dir + f
        etl_538(file_name, conn)
        print('ETL Completed for:', f)
    
    elif f[:2] == "dk":
        file_name = data_dir + f
        etl_dk(file_name, conn)
        print('ETL Completed for:', f)

conn.close()