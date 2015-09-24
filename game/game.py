# written by: Ioannis Paraskevakos
# tested by: Ioannis Paraskevakos
# debugged by: Ioannis Paraskevakos
from __future__ import division
import pymongo
from datetime import date

class Game:
    
    """
        Game Class. This class is used by the play module to update
        the points of an area

        Attributes:
        area : The type of the area. It can be either State or City
        name : The name of the Area
        points : The Number of points that the area has
        tweets : The number of unused tweets for this specific area from the last update
        lastTweetVal : The number of Tweets that were used for the last update
        lastUpdate : This is the date of the last update with tweets.
        totalTweets : The total number of tweets
        motherState : In case of a County in which State it belongs

        __init__() : Class Constractor
        __get__() : returns the value of an attribute
        __set__() : Sets an attribute
        NewPoints : The basic point update method.
    """

    def __init__(self,area='state',name=None,points=0,tweets=None,lastTweetVal=None,lastUpdate=None,totalTweets=None,motherState=None):
        """Class Constructor. The constructor initializes the classes attributes."""
        self.area         = area
        self.name         = name
        self.points       = points
        self.tweets       = tweets
        self.lastTweetVal = lastTweetVal
        self.lastUpdate   = lastUpdate
        self.totalTweets  = totalTweets
        self.motherState  = motherState

    def __get__(self, attr='name'):
        """
        Return the attribute based on the name of the attribute
        """
        if attr == 'area':
            return self.area
        elif attr == 'name':
            return self.name
        elif attr == 'points':
            return self.points
        elif attr == 'tweets':
            return self.tweets
        elif attr == 'lastTweetVal':
            return self.lastTweetVal
        elif attr == 'lastUpdate':
            return self.lastUpdate
        elif attr == 'totalTweets':
            return self.totalTweets
        elif attr == 'motherState':
            return self.motherState
        else:   
            return 0

    def __set__(self, attr,val):
        """
        Set the value of an attribute based on it name with val
        """
        if attr == 'area':
            self.area = val
            return 1
        elif attr == 'name':
            self.name = val
            return 1
        elif attr == 'points':
            self.points = val
            return 1
        elif attr == 'tweets':
            self.tweets = val
            return 1
        elif attr == 'lastTweetVal':
            self.lastTweetVal = val
            return 1
        elif attr == 'lastUpdate':
            self.lastUpdate = val
            return 1
        elif attr == 'totalTweets':
            self.totalTweets = val
            return 1
        elif attr == 'motherState':
            self.motherState = val
            return 1
        else:   
            return 0
        

    def NewPoints(self):
        
        """
        The basic point update method. It updates the points of an area
        based on how often it is updated, when tweets from that area are
        retrieved, what impact those new tweets have in the total
        number of tweets from that area and what is the difference from
        the last update.
        
        """

        TimeNow = date.today() #Get today's date
        TimeDelta = TimeNow - self.lastUpdate # Calculate the difference from last update
        LastTweetCount = self.lastTweetVal
        NewTweetCount = self.tweets
        Update = 0 # Indicates whether an update should happen or not.
               # Value 0 no update, 1 update everything, 2 update only points


        if (TimeDelta.days > 7 and self.tweets == 0 and self.totalTweets != 0 and self.points > 0):
            #If there is no new tweets for a week subtract 10 points and keep last update's
            # date and last tweet count
            EarnedPoints = -10
            Update = 2
        else:
            # At the beginning consider the points to be as many as the new tweets minus the old
            # This way the game system is just, less tweets from last time means loss of points
            EarnedPoints = NewTweetCount - LastTweetCount
            if(self.totalTweets == 0):
                # First Time playing the game! Bonus 20 points
                EarnedPoints = EarnedPoints + 20
                Update = 1
            elif(EarnedPoints >= 0 and NewTweetCount/LastTweetCount >= 1.5 and NewTweetCount/self.totalTweets > 0.1):
                # More than 50% extra tweets and mre than the 10% of all tweets 10 extra points
                EarnedPoints = EarnedPoints + 10
                Update = 1
            elif (EarnedPoints >= 0 and NewTweetCount/LastTweetCount >= 1.5 and NewTweetCount/self.totalTweets <= 0.1):
                # More than 50% extra tweets and less than the 10% of all tweets 5 extra points
                EarnedPoints = EarnedPoints + 5
                Update = 1
            elif (EarnedPoints >= 0 and NewTweetCount/LastTweetCount < 1.5 and NewTweetCount/self.totalTweets > 0.1):
                # Less than 50% extra tweets and mre than the 10% of all tweets 5 extra points
                EarnedPoints = EarnedPoints + 5
                Update = 1
            elif (EarnedPoints >= 0 and NewTweetCount/LastTweetCount < 1.5 and NewTweetCount/self.totalTweets <= 0.1):
                # Less than 50% extra tweets and less than the 10% of all tweets 0 extra points
                Update = 1
            elif (EarnedPoints < 0 and NewTweetCount/LastTweetCount >= 0.5 and NewTweetCount/self.totalTweets > 0.1):
                # Less absolute value and more than 50% tweets and mre than the 10% of all tweets half points
                EarnedPoints = 0.5*EarnedPoints
                Update = 1
            elif (EarnedPoints < 0 and NewTweetCount/LastTweetCount < 0.5 and NewTweetCount/self.totalTweets > 0.1):
                # Less absolute value and less than 50% tweets and m0re than the 10% of all tweets three quarters points        
                EarnedPoints = 0.75*EarnedPoints
                Update = 1
            else:
                # Whatever is at the beginning
                Update = 1

        if (Update == 1):
            #Update everything
            self.points = self.points+EarnedPoints
            self.lastTweetVal = NewTweetCount
            self.totalTweets = self.totalTweets + NewTweetCount
            self.lastUpdate = [TimeNow.year,TimeNow.month,TimeNow.day]
        elif (Update == 2):
            #Update points
            self.points = self.points+EarnedPoints
        



