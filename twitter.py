import tweepy, datetime, time #https://github.com/tweepy/tweepy
import csv, json
from constants import Constants
import json
import re
import pandas as pd
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput

const = Constants()


def get_name (screen_name):
	"""
	Returns the user's name on their twitter account

	Args:

	screen_name : the user's twitter handle

	Returns:

	The user's name on their twitter account
	"""
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(const.twitter_consumer_key, const.twitter_consumer_secret)
	auth.set_access_token(const.twitter_access_key, const.twitter_access_secret)
	api = tweepy.API(auth)

	user = api.get_user(screen_name)
	return user._json['name']
	
def get_all_tweets(screen_name):
	"""
	Extracts the user's tweets

	Args:

	screen_name: the user's twitter handle
       
	"""
	print ()
	print ('Extracting tweets...')
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(const.twitter_consumer_key, const.twitter_consumer_secret)
	auth.set_access_token(const.twitter_access_key, const.twitter_access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []
	count = 20
	deadend = False
	while True:
		tweets = api.user_timeline(screen_name = screen_name,count=count)

		
		for tweet in tweets:
			if (datetime.datetime.now() - tweet.created_at).days > 1: #1= No. of days
				
				alltweets.extend(tweets)
				alltweets. pop()
				deadend = True
				break
		if deadend:
			break
		if not deadend:
		    count+=1
		    
		

	       
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
		
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open( const.tweets_raw % screen_name, mode='w', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)



def get_twitter_emotion(screen_name):
	"""
	Identifies the user's emotion based on their Twitter presence

	Args:

	screen_name: the user's Twitter handle

	Returns:

	The user's emotion as identified
	"""
	get_all_tweets(screen_name)

	print ()
	print ('Identifying mood...')
	service = ToneAnalyzerV3(
	    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
	    # url='https://gateway.watsonplatform.net/tone-analyzer/api',
	    username=const.watson_username,
	    password=const.watson_password,
	    version='2017-09-21')
	
	tweet_df = pd.read_csv(const.tweets_raw % screen_name)

	fh = open(const.tweets_json, "w")
	fh.write(json.dumps({'text':re.sub('\\\\x..', '',r'.'.join([x[2:-1] for x in tweet_df.text]) )}))
	fh.close()
	
	with open(const.tweets_json) as tone_json:
		tone = service.tone(
		    json.load(tone_json)['text'],
		    "text/plain",
		    sentences=True).get_result()
		#print(json.dumps(tone, indent=2))
		
		temp_dict = tone['document_tone']['tones']
		maximum = 0
		emotion = ''
		for x in temp_dict:
			if x['score']>maximum:
				maximum = x['score']
				emotion = x['tone_id']

	return emotion
		


def get_essay_emotion(path):
	"""
	Identifies the user's mood based on a piece of writing authored by them

	Args:

	path: path to the file with text written by the user

	Returns:

	The user's emotion as identified
	"""
	file = open(path, "r")
	text = file.read()
	print ()
	print ('Identifying mood...')
	service = ToneAnalyzerV3(username=const.watson_username,password=const.watson_password,version='2017-09-21')
	service.set_detailed_response(True)
	tone_input = ToneInput(text)
	
	tone = service.tone(tone_input=tone_input, content_type = "application/json")

	emo_score=[]
	for emotion in tone.result["document_tone"]["tones"]:
		print(emotion["score"])
		print(emotion["tone_id"])
		emo_score.append(emotion["score"])
	print(tone.result["document_tone"]["tones"][emo_score.index(max(emo_score))]["tone_id"])
	return(tone.result["document_tone"]["tones"][emo_score.index(max(emo_score))]["tone_id"])  

