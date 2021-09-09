# leveraging_538_for_betting

## Looking for differences in predictions between vegas odds and 538

Before Nate Silver became famous for his political predictions, one of his most notable accomplishments was developing a robust baseball analysis/prediciton, [PECOTA](https://en.wikipedia.org/wiki/PECOTA). To this day, FiveThirtyEight still has a great amount of sports predictions on their [website](https://projects.fivethirtyeight.com/2021-mlb-predictions/games/).

Given Silver's Expereince, Skill, and Previous Sucsess in sports analytics. I want to explore two questions:
 - Is 538's Sports Predictions more accurate than Sports betting institutions?
 - If it is more accurate, can a person generate a profit, by levereging 538?
 
To explore these questions, I plan on:
 - Comparing baseball outcome predictions made by 538 to those implied in Draft Kings moneylines
 - Calculating and comparing the error rates of 538's and Draft Kings predictions
 - Looking at the expected outcomes when multiplying 538's probabilitys by Draft King's moneyline payouts
 - Looking at the short/medium/long term profits (or losses) by betting on games with positive expected outcomes

Throughout this Project I:
 - Created web scrapers to pull data from 538's prediction page and Draft King's moneylines
 - Created an OLTP database to hold those data files
 - Created a data warehouse and corresponding ETL script to load all of the data into one place for analysis
 - Calculated the expected outcome of betting on draft kings moneylines, using an adjusted version of 538's predictions
 - Backtested using all of the scraped baseball data to find out the outcome of betting on games with a positive expected outcome



