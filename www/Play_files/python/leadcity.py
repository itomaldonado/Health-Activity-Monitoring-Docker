# written by: Ioannis Paraskevakos
# tested by: Ioannis Paraskevakos
# debugged by: Ioannis Paraskevakos
from pymongo import MongoClient
from datetime import date
import sys

def get_name_lead(name):
    """
    Arguments
        name : String that is the abbreviation of the state the city leaderboard is
               requested.

    This function opens a client to the database, queries it and gets all the cities
    and sorts them based on their points. Finally it returns the names of the 10 cities
    with the most points
    """
    mongoclient = MongoClient('mongodb://localhost:27017') # Open database connection

    #Get City Collection for the State with name the input and sort the Cities based on their points
    #in ascending order
    CollCounty = mongoclient.search_results[name].find().sort('points') 
    CountyLeadName = list()
    NumOfCounties = CollCounty.count()-1
    # If the cities are more than 10 then select the 10 with the most points
    # else select them all and return their names
    if NumOfCounties >= 9:
        for i in range(0,10):
            CountyLeadName.append(CollCounty[NumOfCounties-i]['name'])
    else:
        for i in range(0,NumOfCounties+1):
            CountyLeadName.append(CollCounty[NumOfCounties-i]['name'])
    
    mongoclient.close() #Close the connection to the database
    return CountyLeadName


def get_point_lead(name):
    """
    Arguments
        name : String that is the abbreviation of the state the city leaderboard is
               requested.

    This function opens a client to the database, queries it and gets all the cities
    and sorts them based on their points. Finally it returns the points of the 10 cities
    with the most points
    """
    mongoclient = MongoClient('mongodb://localhost:27017') # Open database connection

    #Get City Collection for the State with name the input and sort the Cities based on their points
    #in ascending order
    CollCounty = mongoclient.search_results[name].find().sort('points')
    CountyLeadName = list()
    NumOfCounties = CollCounty.count()-1
    # If the cities are more than 10 then select the 10 with the most points
    # else select them all and return their points
    if NumOfCounties >= 9:
        for i in range(0,10):
            CountyLeadName.append(CollCounty[NumOfCounties-i]['points'])
    else:
        for i in range(0,NumOfCounties+1):
            CountyLeadName.append(CollCounty[NumOfCounties-i]['points'])
    
    mongoclient.close() #Close the connection to the database
    return CountyLeadName

if __name__ == '__main__':    

    """
    This program is called from the php file responsible to receive the asynchronous
    request from the webpage. It calls the functions above and then prints the results
    in the standard output.
    """
    #Get the command line argument
    name = sys.argv[1]
    NameLead = get_name_lead(name)
    PointsLead = get_point_lead(name)

    #If the 10 or more cities have been return print the first 10
    #else print everything and fill the gaps with simple spaces.
    Num = NameLead.__len__()
    if Num >= 10:
        for i in range(0,10):
            print NameLead[i]
            print PointsLead[i]
    else:
        for i in range(0,Num):
            print NameLead[i]
            print PointsLead[i]
        for i in range(0,10-Num):
            print ''
            print ''

