# Outline
  * Any key string is inputted by the user and the top 250 tweets relating to the key string are queried using tweepy and the Twitter API, following which a sentiment analysis is conducted on the text of the tweets fetched using TextBlob (v0.16.0). The results are displayed as a pie chart. More detailed description below.

# Purpose
  * The code for this project is very rough around the edges as it was one of my first undertakings in my attempt to teach myself programming and it was extremely useful in understanding the fundamentals of SQL and relational databases as well as in solidifying my knowledge of APIs and Python. Moreover, it helped me understand how to visualise data and its significance. This program could be used by any company or individual to gauge the sentimental response of the general public to their product or marketing.

# Detailed Description
  * The program accepts a user inputted string and queries the Twitter API, using the tweepy.Cursor method, returning the top 250 tweets.
  * Sentiment analysis is then conducted on the results of the query, i.e the tweets using TextBlob (v0.16.0)  and the tweets, along with the sentiment are stored in a relational database using SQL (sqlite3 for Python). The query, analysis and subsequent storage are handled by the load function.
  * The tweets and sentiments are then fetched from the database and analysed, with the program ascertaining a count for each of the sentiments and a proportion as part of the total tweets, with the counts and percent composition being used to create a pie chart to visualise the data. The visualisation is handled by matplotlib.
  * The tweets can be viewed individually using the DB Browser for SQL.

# Important Notes
  * As indicated in the code, the ```from config import *``` is used to import the Twitter API Keys that are needed to query the API using tweepy. The said file is not available in this repo.
  * The software sqlite does have some concurrency issues and cannot operate very heavy tasks and therefore the limit is set to 250 tweets to avoid database locking.
