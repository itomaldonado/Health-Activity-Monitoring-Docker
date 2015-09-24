# written by: Ioannis Paraskevakos
# tested by:
# debugged by:
from pymongo import MongoClient
from hashtable import hashtable
from statehash import StateHash

class Validator:

  '''
  This class is responsible to receive the raw data, find which tweets are actually valid or trusted 
  information based on the criteria the system has and then save them inside the MongoDB.
    
    ** Attributes **
    client : This is the actual connection with the MongoDB
    RawTweets : This is a list that has all the tweets that were grabbed
                more resently from Twitter
    loc_tweets : A list of the Geo Located tweets after the locator method is executed
    good_tweets : A list of the tweets that the first filter let to pass
    final_tweets : A list of the tweets that the filter filter let to pass
    keywords2 : A list with the words used as the filtering terms for the first filter.
                It is read from keywords2.txt file
    keywords3 : A list with the words used as the filtering terms for the first filter.
                It is read from keywords3.txt file

    ** Methods **
    __init__ : The constructor of the class must be present for
               python classes.

    locator : This method checks all tweets and returns only those that are geotagged or uses 
              the location of the user to decide the coordinates of a tweet.
    
    data_filter2 : This method searches through all the Tweets for each word in the keyword
                   list. If a keyword exists in the tweet's text and the tweet has not been
                   added to the final list by a previous keyword success it is added to the
                   tweets that will be returned.

    data_filter3 : This function searches through all the Tweets for each word in the keyword
                   list. If a keyword exists in the tweet's text and the tweet has not been
                   discarded from the final list by a previous keyword success it is discarded
                   from the tweets that will be returned.

    updater : This method just updates the database with the new filtered and located data.
  '''

  def __init__(self):
    '''
    Class Constractor
    '''

    self.client = MongoClient('mongodb://localhost:27017')
    self.RawTweets = self.client.twiter_data.twitter_coll.find()
    self.loc_tweets = list()
    self.good_tweets = list()
    self.final_tweets = list()

    fpK2 = open('keywords2.txt','r')
    fpK3 = open('keywords3.txt','r')
    self.keywords2 = [line.strip() for line in fpK2]
    self.keywords3 = [line.strip() for line in fpK3]
    fpK2.close()
    fpK3.close()



  def locator(self):
    '''
    This method checks all tweets and returns only those that are geotagged or uses 
    the location of the user to decide the coordinates of a tweet.
  
    Arguments:
      self.RawTweets : A list of tweets that will be selected by their location
    
    Output:
      self.loc_tweets : Tweets with coordinates. Each returned tweet has an ID, coordinates,
                   the original tweet's language, the place (City,State), country_code,
                   user information, timestamp in miliseconds.
    '''

    for tweet in self.RawTweets:
      # for all the tweets in the database if a tweet is geotagged keep the necessary information
      # and append it to the located tweets
      if tweet['geo'] != None and tweet['place'] != None:
        finalGeoLat = tweet['geo']['coordinates'][0]
        finalGeoLog = tweet['geo']['coordinates'][1]
        temp_tweet = {'_id':tweet['_id'],'coordinates':[finalGeoLat,finalGeoLog],
                 'lang':tweet['lang'],'text':tweet['text'],
                 'place':tweet['place']['full_name'],
                 'country':tweet['place']['country_code'],
                 'user':tweet['user'],'timestamp_ms':tweet['timestamp_ms']}
        #append tweet
        self.loc_tweets.append(temp_tweet)
      else:
        # Else seach for all the places that coordinates exist in the hashtable
        for place in hashtable:
          # If the user's location is found in the hash table, Geotag the tweet and
          # after changing the state to the abbreviation ppend it to the located
          # tweets
          if tweet['user']['location']==place['name']:
            finalGeoLat = place['lat']
            finalGeoLog = place['long']
            placed = False
            index = 0
            while not placed and index<50:
              #print index
              state = StateHash[index]
  
              # Take the state of the location. If the state is shown with more than two letters
              # chane it with the abbreviation.
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
  
            #append tweet
            self.loc_tweets.append(temp_tweet)


  def data_filter2 (self):
    '''
      This method searches through all the Tweets for each word in the keyword
      list. If a keyword exists in the tweet's text and the tweet has not been
      added to the final list by a previous keyword success it is added to the
      tweets that will be returned.
  
      Arguments:
        self.keywords2: A list of keywords that will be used for the selection
  
        self.loc_tweets: The list with the tweets that need to be filtered.
  
      Output:
        self.good_tweets: A list with all the tweets that contained at least one 
                    keyword
    '''
    # For every tweet
    for tweet in self.loc_tweets:
      #Get the text of the tweet
      text = tweet['text']
      #For every keyword
      for keyword in self.keywords2:
         # If the keyword exists and the tweet has not been selected insert it in
         # the good tweets list
         if keyword in text and tweet not in self.good_tweets:
            self.good_tweets.append(tweet)
    
  
  def data_filter3(self):
    '''
    This method searches through all the Tweets for each word in the keyword
    list. If a keyword exists in the tweet's text and the tweet has not been
    discarded from the final list by a previous keyword success it is discarded
    from the tweets that will be returned.
  
    Arguments:
      self.keywords3: A list of keywords that will be used for the selection
  
      Tweets: The list with the tweets that need to be filtered.
  
    Output:
      self.good_tweets: A list with all the tweets that contained at least one 
                  keyword
    '''

    self.final_tweets = self.good_tweets
  
    # For every tweet
    for tweet in self.good_tweets:
      # Get the text of the tweet
      text = tweet['text']
      # For every keyword
      for keyword in self.keywords3:
        # If the keyword exists and the tweet has not been discarded, remove it
        # from the final tweets
        if keyword in text and tweet in self.final_tweets:
          self.final_tweets.remove(tweet)
  
  def updater(self):
    '''
    This method just updates the database with the new filtered and located data.
    '''

    #In case you only need the located tweets change the self.final_tweets to self.loc_tweets
    for tweet in self.loc_tweets:
      self.client.twiter_data.clean_tweets.update({'_id':tweet['_id']},tweet,True) #Target
  
    #client.twiter_data.twitter_coll.drop()


if __name__ == "__main__":
  '''
    Just run the Class methods.
  '''
  
  Session = Validator()
  Session.locator()
  #Session.data_filter2()
  #Session.data_filter3()
  Session.updater()

