# written by: Ioannis Paraskevakos
# tested by: Ioannis Paraskevakos
# debugged by: Ioannis Paraskevakos
from pymongo import MongoClient
from hashtable import hashtable
from statehash import StateHash

def locator(tweets,hashtable):
  '''
  This function checks all tweets and returns those that are geotagged or 
  the location of the user is recongized and the coordinates are appended to the tweet.

  Arguments:
    tweets : A list of tweets that will be selected by their location

    hashtable : A hashtable containing names of areas and their coordinates

  Output:
    loc_tweets : Tweets with coordinates
  '''

  loc_tweets=list()
  for tweet in tweets:
    #Uncomment this line in case a tweet outside the US passes to find its id
    # and check its location value
    #print tweet['_id']
    if tweet['geo'] != None and tweet['place'] != None:
      finalGeoLat = tweet['geo']['coordinates'][0]
      finalGeoLog = tweet['geo']['coordinates'][1]
      temp_tweet = {'_id':tweet['_id'],'coordinates':[finalGeoLat,finalGeoLog],
               'lang':tweet['lang'],'text':tweet['text'],
               'place':tweet['place']['full_name'],
               'country':tweet['place']['country_code'],
               'user':tweet['user'],'timestamp_ms':tweet['timestamp_ms']}
      loc_tweets.append(temp_tweet)
      #append tweet
    else:
      for place in hashtable:
        if tweet['user']['location']==place['name']:
          finalGeoLat = place['lat']
          finalGeoLog = place['long']
          placed = False
          index = 0
          while not placed and index<50:
            #print index
            state = StateHash[index]
            comma = place['name'].find(',')
            tempstate = place['name'][comma+2:]
            if tempstate.__len__() > 3 and tempstate in state['name']:
              part = place['name'].partition(',')
              new_place = part[0]
              new_place=new_place+', '+state['_id']
              placed = True
            if not placed:
              new_place = place['name']
            index=index+1
          temp_tweet = {'_id':tweet['_id'],'coordinates':[finalGeoLat,finalGeoLog],
               'lang':tweet['lang'],'text':tweet['text'],
               'place':new_place,
               'country':'US',
               'user':tweet['user'],'timestamp_ms':tweet['timestamp_ms']}
          loc_tweets.append(temp_tweet)
          #append tweet

  return loc_tweets

def data_filter2 (keywords, Tweets):
  '''
    This function searches through all the Tweets for each word in the keyword
    list. If a keyword exists in the tweet's text and the tweet has not been
    added to the final list by a previous keyword success it is added to the
    tweets that will be returned.

    Arguments:
      keywords: A list of keywords that will be used for the selection

      Tweets: The list with the tweets that need to be filtered.

    Output:
      good_tweets: A list with all the tweets that contained at least one 
                  keyword
  '''
  good_tweets=list()
  # For every tweet
  for tweet in Tweets:
    #Get the text of the tweet
    text = tweet['text']
    #For every keyword
    for keyword in keywords:
       # If the keyword exists and the tweet has not been selected insert it in
       # the good tweets list
       if keyword in text and tweet not in good_tweets:
          good_tweets.append(tweet)
  
  # Return the Filtered tweets.
  return good_tweets

def data_filter3(keywords,Tweets):
  '''
  This function searches through all the Tweets for each word in the keyword
  list. If a keyword exists in the tweet's text and the tweet has not been
  discarded from the final list by a previous keyword success it is discarded
  from the tweets that will be returned.

  Arguments:
    keywords: A list of keywords that will be used for the selection

    Tweets: The list with the tweets that need to be filtered.

  Output:
    good_tweets: A list with all the tweets that contained at least one 
                keyword
  '''
  final_tweets = list()
  final_tweets = Tweets

  # For every tweet
  for tweet in Tweets:
    # Get the text of the tweet
    text = tweet['text']
    # For every keyword
    for keyword in keywords:
      # If the keyword exists and the tweet has not been discarded, remove it
      # from the final tweets
      if keyword in text and tweet in final_tweets:
        final_tweets.remove(tweet)

  return final_tweets

def data_filtering():
  '''
  This function creates the filtering of the tweets. It has no attributes. 
  It automatically connects to the MongoDB database, fetches all the tweets from
  the United States and then filters them with the keywords that are in the txt
  files keywords1.txt,keywords2.txt and keywords3.txt

  '''


  fpK2 = open('keywords2.txt','r')
  fpK3 = open('keywords3.txt','r')


  keywords2 = [line.strip() for line in fpK2]
  keywords3 = [line.strip() for line in fpK3]

  fpK2.close()
  fpK3.close()

  # Change the Mongo Client argument to the URL of your Mongo DB. If using two
  # databases replicate the following line, change the URL to target database
  # and change to the proper Client the line with the comment "Target" as a
  # suffix
  client = MongoClient('mongodb://localhost:27017')

  RawTweets = client.twiter_data.twitter_coll.find()

  usable_tweet = locator(RawTweets,hashtable)
  tweets_f1 = data_filter2 (keywords2, usable_tweet)
  tweets_final = data_filter3(keywords3,tweets_f1)

  for tweet in tweets_final:
    client.twiter_data.clean_tweets.update({'_id':tweet['_id']},tweet,True) #Target

  client.twiter_data.twitter_coll.drop()

  client.close()
  return True

if __name__ == "__main__":
  '''
    Just run the above functions
  '''
  data_filtering()

