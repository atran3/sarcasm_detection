from os import path
from datetime import datetime

def get(category):
	data = []
	with open("twitter_data/" + category + "CleanData.csv", 'r') as f:
		reader = f.read().split('\x1E')
		for example in reader:
			example = example.split('\x1F')
			if len(example) <= 1: continue
			if example[1] != '':
				example[1] = datetime.strptime(example[1][:-6], "%Y-%m-%d %H:%M:%S")
			if example[3] != '':
				example[3] = datetime.strptime(example[3][:-6], "%Y-%m-%d %H:%M:%S")
			data.append(example)
		return data

