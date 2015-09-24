1) In order to load the web site you need to install the PHP,Apache and MongoDB.
   Here is a tutorialon how to do it in Ubuntu :
   http://tecadmin.net/setup-mongodb-php5-apache2-ubuntu/
   After finishing the steps in the above url, just copy everything from the www
   folder under /var/www/html and everything is done
2)Before running the CalorieMeter for the first time, the following packages must be downloaded using the following command:
  pip install twitter
  pip install prettytable
  pip install json
  pip install Counters
  Then, simply the code could be compiled using the following command:
  python CalorieMeter.py
  
3)To implement the interactive map you have to follow these steps:

A)to make this code work, first, you have to install the following software:

Python   (www.python.org)
MongoDB  (www.mongodb.org)
redis server (www.redis.io)
Flask (flask.pocoo.org)
Tweepy (www.tweepy.org)

B)Then you have to make this configuration:

Twitter Streaming API credentials (you have to register at twitter development website dev.twitter.com)
create a capped collection in MongoDB named "tweets" using the following query: db.createCollection("log", { capped : true, size : 5242880, max : 5000 })

c)Now, follow these steps to make it work (bash commands in the parenthesis):

start MongoDB ($ mongod).
start Redis server ($ redis-server).
execute ‘twitter_stream.py’ ($ python twitter_stream.py)
execute ‘data.py’ ($ python data.py)
open the map.html (write in the web browser address: localhost:5000/map.html). You have to be connected to the Internet during the execution time.
A google map will be shown in the page and the data will be appear on the map gradually. 

3) In order to run the Game Feature, assuming that all the servers are up and running, instruction 3 from ../4_data_collection/README4.txt, go to the game folder and type:
    python Play.py
   After a while the program will end and you will be able to see the points in the web page.

4) If you have downloaded the data from our online database and you want to run the filtering proccess, then:
   1) In line 156 of the data_filtering.py file client.<db_name>.<coll_name>.find() the db_name and coll_name are the same with your database.
   2) If you do not want to use the filters, but only the locator comment lines 140-148, lines 159-160 and change in line 162 tweets_final to usable_tweets
   3) To run type python data_filtering.py