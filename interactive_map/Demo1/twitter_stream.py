import tweepy
import json
from pymongo import Connection
from bson import json_util
from tweepy.utils import import_simplejson

json = import_simplejson()
mongocon = Connection()

db = mongocon.twiter_data
col = db.tweets_stream

consumer_key = 'AYh6x5HIt5ubprSXeEGVqmLnT'
consumer_secret = 'wx4wC2ttf3hS34iGPMeL6VAifwIZ7AOCbqT9Z4Vri0ZQPDhQrF'

access_token_key = '92291123-Wysxd5FnzMAKZWBQzFlExWRrq6kSduWd78J9TYlpk'
access_token_secret = 'stP7FrAwohkVmo3HYZ3oRUqm1jcgvVK9rZubEVX7Tlreq'

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
    mongocon = Connection()
    db = mongocon.tstream
    col = db.tweets
    json = import_simplejson()

    
    def on_status(self, tweet):
        print 'Ran on_status'

    def on_error(self, status_code):
        return False

    def on_data(self, data):
        if data[0].isdigit():
            pass
        else:
            col.insert(json.loads(data))
            print(json.loads(data))

l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
setTerms = ['#CrossFit', '#loseit', 'twitter']
streamer.filter(track = setTerms)
