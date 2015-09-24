from CityPopHash import CityPopHash  # i may not need this?
from PerCapitaAssignWeights import *

#Call this function after the tweets have been cleaned.
#This will take tweets from the clean_tweets collection,
# take only the lat and log coordinates, apply them to the 
# weight function, then save the lat, log, and weight in
# a collection named "per_capita_tweets" in the same database.

def percapitafilter(client):
	fetchedData = client.twitter_data.clean_tweets.find()
	for fetched in fetchedData:
		log = fetched['finalGeoLog']
		lat = fetched['finalGeoLat']
		weight = PerCapitaAssignWeights(lat,log)
		temporaryTweet = {'lat':lat,'log':log,'weight':weight}
		client.twitter_data.per_cap_tweets.insert(temporaryTweet)