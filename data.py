from datetime import datetime
import json

def get(category):
	data = []
	with open("twitter_data/" + category + "Featurized.csv", 'r') as f:
		all_features = json.load(f)
		for features in all_features:
			if features.get('TEXT_TIME', False):
				features['TEXT_TIME'] = datetime.strptime(features['TEXT_TIME'][:-6], "%Y-%m-%d %H:%M:%S")
			if features.get('REPLY_TIME', False):
				features['REPLY_TIME'] = datetime.strptime(features['REPLY_TIME'][:-6], "%Y-%m-%d %H:%M:%S")
			data.append(features)
		return data

