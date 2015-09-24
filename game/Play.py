# written by: Ioannis Paraskevakos
# tested by: Ioannis Paraskevakos
# debugged by: Ioannis Paraskevakos

from __future__ import division
from pymongo import MongoClient
from datetime import date
from game import Game

class Play:
	
    """
    This Class is the Class that conects MongoDB with the
    Game class. Contains all the necessary the methods to enable the game.
    
    ** *Attributes* **
        mongoclient   : This is the actual connection with the MongoDB
        CollState     : This is the connection with the Collection that
                        holds the data for the Game over the States.
        CollTwets     : This is the connection with the Collection that 
                        holds the data from the tweets pulled from Twitter
        TweetedStates : This attribute has a list of the states mentioned
                        in the Tweets
        TweetedCities : This attribute has a list of the states mentioned
                        in the Tweets

        ** *Methods* **
           __init__ : The constructor of the class must be present for
                      python classes.

           grab_tweets  : This method is to utilize the existing connection
                          with the database and get the needed data

           update_areas : This method is used to call the game class and update
                         the database entry for that specific area.
    """
    def __init__(self):
        """
        Class Constructor
        """
        self.mongoclient = MongoClient('mongodb://localhost:27017') # Creates aa connection to MongoDB
        self.CollState = self.mongoclient.search_results.States #Get State collection from search_results database
        self.CollTweets = self.mongoclient.twiter_data.clean_tweets #Get raw_data collection from search_results database
        self.TweetedStates = dict()
        self.TweetedCities = dict()

    def grab_tweets(self):
        """
        This method is responsible to query the database and count the number of tweets
        for each state that has new tweets and each city. 
        """
        Tweets = self.CollTweets.find() # Find the tweet that have geo coordinates for the moment.
        index = 0
        for tweet in Tweets:
            place = tweet['place']
            country = tweet['country']
            state = place[-2:]
            index = index + 1
            #If the states is already found increment the number of tweets
            #for this state else put 1 since this is the first tweet
            AreaEntry = self.CollState.find_one({'_id':state})
            if AreaEntry:
                if (self.TweetedStates.__contains__(state) and country=='US' and state!='US'):
                    self.TweetedStates[state] = self.TweetedStates[state]+1
                elif (state!='US' and country == 'US'):
                    self.TweetedStates[state] = 1
                if (self.TweetedCities.__contains__(place) and country=='US' and state!='US'):
                    self.TweetedCities[place] = self.TweetedCities[place]+1
                elif (state!='US' and country == 'US'):
                    self.TweetedCities[place] = 1


    def update_areas(self):
        '''
        This method is responsible to go through the two area dictionaries,
        create a Game object of the Game Class for a given area and run the
        game.

        At the end it should update the database for that area.
        '''

        #First update States
        for state in self.TweetedStates:
            print state
            # Query the database for the state with id its name.
            AreaEntry = self.CollState.find_one({'_id':state})
            #Grad the date of the last update, create an object of the Game
            #class and call the method for the new points
            lastdate = date(AreaEntry['lastUpdate'][0],AreaEntry['lastUpdate'][1],AreaEntry['lastUpdate'][2]) #extract last update date
            GamingArea = Game('state',AreaEntry['name'],AreaEntry['points'],self.TweetedStates[state],AreaEntry['lastTweetVal'],
                lastdate,AreaEntry['totalTweets'])
            GamingArea.NewPoints()
            #Change the values of the database entry based on the decisions
            #made by the Game class object
            AreaEntry['points']=GamingArea.__get__('points')
            AreaEntry['lastTweetVal'] = GamingArea.__get__('lastTweetVal')
            AreaEntry['lastUpdate'] = GamingArea.__get__('lastUpdate')
            AreaEntry['totalTweets'] = GamingArea.__get__('totalTweets')
            self.CollState.update({'_id':AreaEntry['_id']},AreaEntry,True)

        for city in self.TweetedCities:
            motherstate = city[-2:]
            name = city[0:-4]
            # Query the database for the state with id the motherstate
            # By taking the name field the proper collection for the
            # the City leaderboard is selected.
            state = self.CollState.find_one({'_id':motherstate})
            CollCity = self.mongoclient.search_results[motherstate]
            AreaEntry = CollCity.find_one({'name':name})
            adding_entry = 0
            # If the city does not exist create a new entry with the necessary starting data
            if not AreaEntry:
                AreaEntry = dict()
                AreaEntry['area'] = 'city'
                AreaEntry['name'] = name
                AreaEntry['points'] = 0
                AreaEntry['lastTweetVal'] = 0
                AreaEntry['lastUpdate'] = [date.today().year,date.today().month,date.today().day]
                AreaEntry['totalTweets'] = 0
                AreaEntry['motherState'] = motherstate
                adding_entry = 1
                
            #Grad the date of the last update, create an object of the Game
            #class and call the method for the new points
            lastdate = date(AreaEntry['lastUpdate'][0],AreaEntry['lastUpdate'][1],AreaEntry['lastUpdate'][2]) #extract last update date
            GamingArea = Game('city',AreaEntry['name'],AreaEntry['points'],self.TweetedCities[city],AreaEntry['lastTweetVal'],lastdate,AreaEntry['totalTweets'],motherstate)

            GamingArea.NewPoints()
            #Change the values of the database entry based on the decisions
            #made by the Game class object
            AreaEntry['points']=GamingArea.__get__('points')
            AreaEntry['lastTweetVal'] = GamingArea.__get__('lastTweetVal')
            AreaEntry['lastUpdate'] = GamingArea.__get__('lastUpdate')
            AreaEntry['totalTweets'] = GamingArea.__get__('totalTweets')

            #If the entry is new insert it to MongoDB, else update it
            if adding_entry:
                CollCity.insert(AreaEntry)
            else:
                CollCity.update({'_id':AreaEntry['_id']},AreaEntry,True)

	
if __name__ == '__main__':
	
    print "Starting Game Phase"

    Session = Play()
    Session.grab_tweets()
    Session.update_areas()
