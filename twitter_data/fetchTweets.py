import os, sys
import httplib, urllib
import json

FILES = ["educationIDs.txt", "ironyIDs.txt", "newspaperIDs.txt", "politicsIDs.txt", "humourIDs.txt", "sarcasmIDs.txt"]

def loadData(data, outfile):
	for datum in data:
		json.dump(datum, outfile)
		outfile.write('\n')

def fetchTweets(infile, outfile, conn):
	l = list()
	# counter = 0
	with open(infile, 'r') as inf:
		for line in inf:		
			if len(l) < 100:
				l.append(line.strip())
			if len(l) == 100:
				# counter += 100
				j = ",".join(l)
				data = json.loads(makeRequest(conn, urllib.urlencode({"id": ",".join(l)})))
				loadData(data, outfile)
				# print "successfully loaded" + str(counter) + "lines!"
				l = [line]

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
		with open(infile.split('IDs')[0] + "Tweets.json", 'w') as outfile:
			fetchTweets(infile, outfile, conn)
			# print "finished" + infile + "!"

if __name__ == "__main__":
	main()

# curl --data "grant_type=client_credentials" -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -H "Authorization: Basic eHpDZ0l6RndBSG1EWVpFb3JYUUhkQ0hiSTpRME52bEw2UjltcjQ5Y04xcWJ4Y0FGZU9ld29UbFhZWnpYUXlmWmFGdWJRZG15V2NTcg==" https://api.twitter.com/oauth2/token

# curl -H "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAEY2vQAAAAAAbkUzQIDIdIunCIazpD%2FNnBeyM0s%3DXnIlgmZjMYMFlxJvDJRC335GGbbRd59yAegtJw65KqEsM8qyws" https://api.twitter.com/1.1/statuses/lookup.json?id=20,432656548536401920