import tweepy #pip install tweepy if no module found - OR If you are using Anaconda try $ conda install -c conda-forge tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys

#uncomment below to start from today, if not specify a date (YYYY, M, D)
#DATE = datetime.now()
DATE = datetime(2018, 4, 4)

date = DATE

datestrTodayFile = str(date.day)+ "-" + str(date.month) + "-" +  str(date.year) #file datestring

print("Gathering tweets for " + datestrTodayFile)

#today auth tweepy format
date = datetime.now()
datestrToday = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

#yesterday auth tweepy format
date = date - timedelta(1)
datestrYesterday = str(date.year) + "-" + str(date.month) + "-" + str(date.day)



## Insert your API keys and tokens below, go to https://apps.twitter.com and create an app if you need one

#Consumer Key (API Key)
consumerKey = ""
#Consumer Secret (API Secret)
consumerSecret = ""
#Access Token
accessToken = ""
#Access Token Secret
accessTokenSecret = ""

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

MAX_TWEETS = 2000

api = tweepy.API(auth)



import csv   
import os

# predefined dictionaries as features
DICTIONARY=["sick", "ill", "not feeling well", "sick at home", "cough", "fever", "headache"]

places = api.geo_search(query="Australia", granularity="country", since=datestrYesterday, until=datestrToday)
place_id = places[0].id

## create long query string
queries = []
for word in FEATURES:
    queries.append("place:%s" % place_id +  " \"" + word + "\"")
    

## setup CSV
## create one for today if it doesn't exist
filename = 'Tweets/' + datestrTodayFile+'.csv'

api = tweepy.API(auth)
places = api.geo_search(query="Australia", granularity="country", since=datestrYesterday, until=datestrToday)
place_id = places[0].id


## gets all the tweets for the features definated above
def get_tweets(): 
    for query in queries:
        print("Gathering tweets for " + query)
        
        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        try:
            tweets = api.search(q=query, tweet_mode='extended')

            with open(filename, append_write, newline='', encoding='utf-8') as c: 
                writer = csv.writer(c)
                if append_write == 'w': # new file
                    writer.writerow(["text", "id"]) #append column title
                    
                count = 0 # number of tweets found in this feature

                for tweet in tweets:

                    ## ensure string is one one line, for proper compliation
                    tweetText = tweet.full_text.replace('\n', ' ').replace('\r', '')

                    writer.writerow([tweetText, tweet.id])
                    print ("feature: " + query + ", " + tweet.full_text + " | " + tweet.place.name if tweet.place else "Undefined place \n") 
                    count = count + 1
            
            print("Found " + str(count) + " tweets containing /'" + query + "'/")
        except:
            print("Too many requests, waiting 15 minutes..") #twitter 88 error code - wait 15 minutes
            time.sleep(60 * 15) # wait 15 minutes

    #s.enter(1, 1, get_tweets, (sc,)) # wait before going again, unless we are at 1000

get_tweets()


