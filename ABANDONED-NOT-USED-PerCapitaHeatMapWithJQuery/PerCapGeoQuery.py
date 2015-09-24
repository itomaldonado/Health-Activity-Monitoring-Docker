from pymongo import MongoClient
from datetime import date
import json
def GetGeoData():
	mongoclient = MongoClient('mongodb://localhost:27017')
	GeoData = mongoclient.twitterdean.deansfilteredtweets.find().limit(1000)

	return GeoData


if __name__ == '__main__':
	GeoCoordinateData = GetGeoData()
	for parts in GeoCoordinateData:
		print (parts)
