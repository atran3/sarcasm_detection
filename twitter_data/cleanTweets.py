import os, sys
import httplib, urllib
import json
import pytz
from datetime import datetime

FILES = ["educationTweets.json", "ironyTweets.json", "newspaperTweets.json", "politicsTweets.json", "humourTweets.json", "sarcasmTweets.json"]

def cleanText(text, entities, category):
	cleanText = text
	hashtags = entities.get('hashtags', [])
	ranges = []
	for hashtag in hashtags:
		if hashtag.get('text', '').lower() == category:
			indices = hashtag.get('indices')
			ranges.append(indices)
	urls = entities.get('urls', [])
	urls.reverse()
	ranges.extend([v for url in urls for k,v in url.iteritems() if k == 'indices'])
	media = entities.get('media', [])
	media.reverse()
	ranges.extend([v for medium in media for k,v in medium.iteritems() if k == 'indices'])
	ranges = sorted(ranges, key=lambda x: x[0], reverse=True)
	for r in ranges:
		cleanText = cleanText[:r[0]] + cleanText[r[1] + 1:]
	return cleanText

def cleanJSON(infile, outfile, conn, category):
	with open(infile, 'r') as inf:
		# counter = 0
		for line in inf:
			tweet = json.loads(line)
			text = tweet.get('text', '')
			entities = tweet.get('entities', {})
			text = cleanText(text, entities, category)
			created_at = tweet.get('created_at', None)
			time = ''
			if created_at is not None:
				time = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
			reply_to = tweet.get('in_reply_to_status_id', None)
			reply_time = ''
			reply_text = ''
			if reply_to is not None:
				data = json.loads(makeRequest(conn, urllib.urlencode({"id": reply_to})))
				if data != []:
					reply_tweet = data[0]
					reply_text = reply_tweet.get('text', '')
					reply_entities = reply_tweet.get('entities', {})
					reply_text = cleanText(reply_text, reply_entities, category)
					reply_created_at = reply_tweet.get('created_at', None)
					if reply_created_at is not None:
						reply_time = datetime.strptime(reply_created_at,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
			data = [text, time, reply_text, reply_time]
			try:
				outfile.write('\x1F'.join(map(str, data)) + '\x1E')
				# counter += 1
				# print "successfully written" + str(counter) + "tweets!!"
			except:
				continue

def makeRequest(conn, params):
	headers = {"Content-type": "application/x-www-form-urlencoded",
			   "Authorization": "Bearer " + os.environ.get('TWITTER_ACCESS', None)}
	conn.request("POST", "/1.1/statuses/lookup.json", params, headers)
	response = conn.getresponse()
	data = response.read()
	return data

def main():
	conn = httplib.HTTPSConnection("api.twitter.com")
	global FILES
	for infile in FILES:
		category = infile.split('Tweets')[0]
		with open(category + "CleanData.csv", 'w') as outfile:
			cleanJSON(infile, outfile, conn, category)
			# print "finished" + infile + "!"

if __name__ == "__main__":
	main()