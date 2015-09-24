#This is the function that will assign a weight to each set of coordinates.
	###PLEASE NOTE- The weight that we want to assign to each coordinate is 
	#the inverse of the population.  This allows smaller populations to be
	#weighted higher for each tweet.  HOWEVER, due to a quirk in google maps,
	#we must also multiply that inverse by the highest population number,"maxPop" 
	#which happens to be New York's population####

#It will be applied on the server side, at the time when I am saving the coordinates.
#It will be applied AFTER the city name algorithm is applied to the raw tweets.
# to a smaller collection.  I will want to save the latitude, longitude, and the weight,
# to the smaller collection.  This function will be used to find the weight.

#import the table containing the top cities with coordinates and population before using this.
from CityPopHash import *
from math import radians, cos, sin, asin, sqrt, fabs

#This function calculates the distance between 2 sets of geo coordinates
#We will use this inside of our PerCapitaAssignWeights function below.
def haversine(lon1, lat1, lon2, lat2):
    
    #Calculate the great circle distance between two points 
    #on the earth (specified in decimal degrees)
    
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 3960 miles is the radius of the Earth
    miles = 3960 * c
    return miles 
	
def PerCapitaAssignWeights(geoLat, geoLog, radiusInfluence = 120, minPop = 3000, maxPop = 8363710):
#This function takes as arguments, a pair of geoCoordinates from MongoDB in the format above,
#It also takes a table with Lat, Log, and Population data as CityPopHash.
#It also takes a radius of Influence, which is the mileage radius from the lat, long pair
#	within which, any city from our hash-like table, will be included into the function for 
#	calculating the approximate population of different lat,long coordinates.  Default is 100 miles
#It also takes a minimum Population number, in the event that a tweet is received from an area in 
#	which a tweet is received is more than 100 miles from any city.  It's default is 1000.
#It also takes a maxPop number which is used to multiply the weights due to Google Map's 
# inability to deal with small fractions as weights.

	nearbyCitiesList=[]
	
	#To be efficient, we first want to iterate through the entire hashtable, to see if 
	#the geoData is located in that city. If the exact coordinates are in the hashtable, then we break the for loop
	# and we can assign the population weight directly
	for city in CityPopHash:		#iterate through each city in the table
		cityLat = city['lat']
		cityLog = city['log']
		if ((geoLat == cityLat) and (geoLog == cityLog)):
			#Then this tweet is from a defined city in the able and we assign that city's exact pop weight
			#WRITE BEHAVIOR HERE!!!! Assign weight to coordinate
			cityPop = city['pop']
			#if we have located the exact coordinates, there is no need to check the other cities.
			return maxPop/cityPop
	#Now, we check if we found the city first, then we re-loop through the cities to 	
	# find our estimated population, using our algorithm
	#We split these 2 loops because computationally, this loop is much more expensive.

	for city in CityPopHash:
		cityLat = city['lat']
		cityLog = city['log']
		#We are going to use an AND statement to take advantage of efficiencies with the short
		# circuit feature.  If the lat or long of a city, by itself, is far enough away from the 
		# geo data, then we can discard it without having to waste computation time on the distance
		# calculation function.  
		if (fabs(cityLat-geoLat) < (radiusInfluence/70.0) and 
			fabs(cityLog-geoLog) < (radiusInfluence/50.0) and
			haversine(geoLog,geoLat,cityLog,cityLat) < radiusInfluence):
			#Here we need to save the population number and the distance from the city all the cities from the CityPopHash that 
			cityDist = haversine(geoLog,geoLat,cityLog,cityLat)
			cityPop = city['pop']
			p = [cityDist, cityPop]
			nearbyCitiesList.append(p)

	#Now we are going to calculate the estimated population from 		
	countOfCities = len(nearbyCitiesList)
	if(countOfCities == 0):
		return maxPop/1000000 #This assumes that a tweet coming from a place that is near no cities with be downweighted
		#so that it is equivalent to a population of one million.  
	

	#We are going to find the closest city to the coordinate. 
	#Every other city is going to be weighted inversely to the ratio of its distance to the dist of the nearest city
	currentMin = radiusInfluence  # start the min at the biggest dist possible
	#loop through all the nearby cities to find the closest one
	for city in nearbyCitiesList:
		temp = city[0]
		currentMin = min(currentMin,temp)
	totalNearbyWeight = 0.0 #this is the sum total of the weights allocated to each nearby city
	totalNearbyPop = 0.0 	#this is the sum total of each calculated weight
	#This for loop does the following:
	#1. It sets the highest weight possible (1) to the closest city to our geo tags
	#2. Every other city is given a weight that is the selected as the distance of the closest city divided by 
	# the distance of city x from our geoTags.  This is then raised to a power of 2.4, in order to exaggerate the 
	# impact of the closes cities.  Also, to prevent areas nearby large cities from having
	# densely populated outskirts that are not properly accounted for, we introduce the bigCityMultiplier
	# this causes tweets near big cities to have their population lean more towards that of the big city.  
	# We slightly dampen this effect by raising the ratio to the power of .8
	# The 2.4,0.8, and 300000 are 3 variables that should be calibrated in the future.
	for city in nearbyCitiesList:
		theDist = city[0]
		thePop = city[1]
		bigCityMultiplier = max(thePop,300000)  
		nearbyWeight = ((bigCityMultiplier/300000)**0.8)*(currentMin/theDist)**(2.4)
		totalNearbyWeight = totalNearbyWeight + nearbyWeight
		PopContribution =  nearbyWeight*thePop
		totalNearbyPop = totalNearbyPop + PopContribution
	CalcedPop = totalNearbyPop/totalNearbyWeight
	
	return maxPop/CalcedPop
		
		



