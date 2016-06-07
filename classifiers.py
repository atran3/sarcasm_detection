from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
import re
import copy

def read_trends():
	f = open("trends_data/trends.txt")
	trends = {}
	trend2cat = {}
	for line in f.readlines():
		line = line[:-1]
		date, category, trend = line.split('\t')
		if date not in trends:
			trends[date] = []
 
 		trends[date].append(trend)
 		trend2cat[trend] = category

 	return trends, trend2cat


trends, trend2cat = read_trends()

def baseline_phi(features):
	feats = {}
	for string in features['TEXT'].split(' '):
		feats[string] = feats.get(string, 0) + 1
	return feats

def novel_phi(features):
	date1 = features['TEXT_TIME'].strftime("%Y%m")
	hasDate = date1 in trends
	for string in features['TEXT'].split(' '):

		if hasDate and string in trends:
			cat = 'TRENDS_' + trend2cat[string]
			features[cat] = features.get(cat, 0) + 1

	return features

def binary_class_func(y):
	if y == 0:
		return "neutral"
	elif y == 1:
		return "sarcastic"
	else:
		return None

def build_dataset(data, phi, vectorizer=None):
	feat_dicts = []
	raw_examples = []
	for basicFeatures in data:
		raw_examples.append(basicFeatures['TEXT'])
		features = copy.deepcopy(basicFeatures)
		if features.get('TEXT', False): del features['TEXT']
		if features.get('TEXT_TIME', False): del features['TEXT_TIME']
		if features.get('REPLY_TEXT', False): del features['REPLY_TEXT']
		if features.get('REPLY_TIME', False): del features['REPLY_TIME']
		features = phi(features)
		feat_dicts.append(features)
	feat_matrix = None
	# In training, we want a new vectorizer:    
	if vectorizer == None:
		vectorizer = DictVectorizer(sparse=True)
		feat_matrix = vectorizer.fit_transform(feat_dicts)
	# In assessment, we featurize using the existing vectorizer:
	else:
		feat_matrix = vectorizer.transform(feat_dicts)
	return {'X': feat_matrix,
			'vectorizer': vectorizer, 
			'raw_examples': raw_examples}

def print_weights(self):
	weights = list(self.mod.coef_[0])
	fm =  self.vectorizer.inverse_transform(weights)[0]
	fm = sorted(fm.iteritems(), key= lambda x: x[1], reverse=True)
	print "Feature weights:"
	for k,v in fm[:10]:
		print "\t%s\t%f" % (k,v)
	print "\t."
	print "\t."
	print "\t."
	for k,v in fm[-10:]:
		print "\t%s\t%f" % (k,v)


# Logistic Regression on bag of words
class Baseline():
	def __init__(self):
		self.mod = LogisticRegression(fit_intercept = True)

	def train(self, X, Y):
		dataset = build_dataset(X, baseline_phi)
		self.mod.fit(dataset['X'], Y)
		self.vectorizer = dataset['vectorizer']

	def predict(self, X):
		dataset = build_dataset(X, baseline_phi, vectorizer=self.vectorizer)
		return self.mod.predict(dataset['X'])

	print_weights = print_weights


class Novel():
	def __init__(self):
		self.mod = LogisticRegression(fit_intercept = True)

	def train(self, X, Y):
		dataset = build_dataset(X, novel_phi)
		self.mod.fit(dataset['X'], Y)
		self.vectorizer = dataset['vectorizer']

	def predict(self, X):
		dataset = build_dataset(X, novel_phi, vectorizer=self.vectorizer)
		return self.mod.predict(dataset['X'])

	print_weights = print_weights


