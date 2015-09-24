#// written by: Ghassan Bati (ghassan.bati@rutgers.edu)
#// tested by: Ghassan Bati (ghassan.bati@rutgers.edu) 
#// debugged by: Ghassan Bati (ghassan.bati@rutgers.edu)

import twitter
import json
def oauth_login():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information 
    # on Twitter's OAuth implementation.
          
    CONSUMER_KEY = 'iJO2XOwZJ5WP2kfj9eVbog'
    CONSUMER_SECRET = 'vMCSs92TbTwwQ7tDmZBh300Umaq1QArOHvHOBera4'
    OAUTH_TOKEN = '38352410-dcdDMqHrWBqSCacYfB06zxUFCUnPK0qhXdTdkThHs'
    OAUTH_TOKEN_SECRET = 'axYP9IUGGBPgBamCEwdR58QMR0h6NbbjkHF9WxvOoyX2Z'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
# Sample usage
twitter_api = oauth_login()    
# Nothing to see by displaying twitter_api except that it's now a
# defined variable
print twitter_api
###############
q = 'spent #LoseIt' # CalorieMeter intresting keywords and hashtags
count = 100
# See https://dev.twitter.com/docs/api/1.1/get/search/tweets for more details
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']
# Iterate through 5 more batches of results by following the cursor
for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist
        break
    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']
####################
status_texts = [ status['text'] 
                 for status in statuses ]
screen_names = [ user_mention['screen_name'] 
                 for status in statuses
                     for user_mention in status['entities']['user_mentions'] ]
hashtags = [ hashtag['text'] 
             for status in statuses
                 for hashtag in status['entities']['hashtags'] ]
# Compute a collection of all words from all tweets
words = [ w 
          for t in status_texts 
              for w in t.split() ]

# Explore the first 5 items for each...
print json.dumps(status_texts[0:5], indent=1)
print json.dumps(screen_names[0:5], indent=1) 
print json.dumps(hashtags[0:5], indent=1)
print json.dumps(words[0:5], indent=1)
##########################

from collections import Counter
for item in [words, screen_names, hashtags]:
    c = Counter(item)

##########################

from prettytable import PrettyTable

for label, data in (('Word', words), 
                    ('Screen Name', screen_names), 
                    ('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count']) 
    c = Counter(data)
    [ pt.add_row(kv) for kv in c.most_common()[:10] ]
    pt.align[label], pt.align['Count'] = 'l', 'r' # Set column alignment
    print pt
	####
# Specifying where the number of calories is and calculate the total 
str1= "calories";		
jwdah = 0.0;
for t in status_texts:
	print str(t);	
	#print str(t).find(str1);
	ghas= str(t).find(str1);
	bati=ghas-5;
	farouq=str(t)[bati:ghas];
	print farouq
	#print farouq[0]
	import re
	if farouq[0] == " " or farouq[0] == "0" or farouq[0] == "1" or farouq[0] == "2" or farouq[0] == "3" or farouq[0] == "4" or farouq[0] == "5" or farouq[0] == "6" or farouq[0] == "7" or farouq[0] == "8" or farouq[0] == "9":
		jwdah = jwdah + float(str(t)[bati:ghas]);
		print jwdah
	elif farouq[0] == ",":
		jwdah = jwdah + float(str(t)[bati+1:ghas])+1000;
		print jwdah
	elif farouq[0] == ".":
		jwdah = jwdah + float(str(t)[bati+2:ghas]);
		print jwdah
#
print jwdah; # Total of burnt Calories for the most recent 200 tweets