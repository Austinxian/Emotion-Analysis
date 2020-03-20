import tweepy
from pymongo import MongoClient

API_key = "lvCT2sjD97n9rFmWzglVb17Nv"

API_secret_key = "pyU48yQEiKyj8tjTTVqIWqp3eMmpBwvIPQVIFlEqdhrKVaW5na"

Access_token = "1231709419358031873-wljxuiOHSzUnq5AZA27DXNsVASWkll"

Access_token_secret = "pVeLMTDe9Lst8V7kqnHRrODrFmrcT6TjzOv1OPZJjohQt"

auth = tweepy.OAuthHandler(API_key, API_secret_key)

auth.set_access_token(Access_token, Access_token_secret)

api = tweepy.API(auth)

#This is for data crawl, and the data will be stored in the mongo Database

catalogue = ["#excitement OR #exciting", "#happy OR #joy OR #love OR #grateful", "#pleasant OR #admiring OR #trusty OR #comfortable OR #believe", "#surprise OR #astonish OR #shock", "#fear OR #afraid OR #scare", "#angry OR #mad OR #annoyed"]

emotions = ['excitement_collection', 'happy_collection', 'pleasant_collection', 'surprise_collection', 'fear_collection', 'angry_collection']

for type, emotion in zip(catalogue, emotions):

    for tweet in tweepy.Cursor(api.search, q=type+' -filter:retweets', lang='en', tweet_mode='extended').items(200):
            client = MongoClient('localhost', 27017)
            db = client['twitter_db1']
            collection = db[emotion]
            collection.insert(tweet._json)







