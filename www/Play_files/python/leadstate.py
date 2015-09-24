# written by: Ioannis Paraskevakos
# tested by: Ioannis Paraskevakos
# debugged by: Ioannis Paraskevakos
from pymongo import MongoClient
from datetime import date

def get_name_lead():
    """
    This function opens a client to the database, queries it and gets all the states
    and sorts them based on their points. Finally it returns the names of the 10 states
    with the most points
    """
    mongoclient = MongoClient('mongodb://localhost:27017') #Open MongoDB connection
    
    #Query database for the States and sort them in Ascending order
    CollState = mongoclient.search_results.States.find().sort('points')
    StateLeadName = list()

    # Create a list with the names of the Ten states with the most points in descendin order
    for i in range(0,10):
        StateLeadName.append(CollState[49-i]['name'])

    mongoclient.close() #Close the connection to the database    
    return StateLeadName


def get_point_lead():
    """
    This function opens a client to the database, queries it and gets all the states
    and sorts them based on their points. Finally it returns the points of the 10 states
    with the most points
    """
    mongoclient = MongoClient('mongodb://localhost:27017')#Open MongoDB connection

    #Query database for the States and sort them in Ascending order
    CollState = mongoclient.search_results.States.find().sort('points')
    StateLeadPoints = list()
    
    # Create a list with the points of the Ten states with the most points in descendin order
    for i in range(0,10):
        StateLeadPoints.append(CollState[49-i]['points'])
    
    mongoclient.close() #Close the connection to the database
    return StateLeadPoints

if __name__ == '__main__':

    """
    This program is called from the php file responsible to receive the asynchronous
    request from the webpage. It calls the functions above and then prints the results
    in the standard output.
    """
    
    NameLead = get_name_lead()
    PointsLead = get_point_lead()

    for i in range (0,10):  
        print NameLead[i]
        print PointsLead[i]
