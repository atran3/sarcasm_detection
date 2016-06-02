from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from nltk.corpus import wordnet as wn
import re

def baseline_phi(text1, time1, text2, time2):
	feats = {}

	#laugh words
	num_laugh_words = len(re.findall(r'lol|haha|hahaha|rofl|lmao', text1))
	# num_emoticons = len(re.findall(r'\:\)|\:\(|\;\)|\:D', text1))

	#capitalization
	num_capital_words = 0
	num_all_caps = 0

	#punctuation
	num_ellipsis = len(re.findall(r'\.\.\.', text1))
	num_exclamation_points = len([1 for ch in text1 if ch == '!'])
	num_punctuation_marks = len([1 for ch in text1 if ch in ['!', ',', '.', '?', '"', ';', '-']])

	#word structure
	num_words = len(text1.split(' '))
	mean_word_length = 0
	mean_synsets = 0
	max_synset = 0

	for string in text1.split(' '):
		len_synset = len(wn.synsets(string))
		if len_synset > max_synset: max_synset = len_synset
		mean_synsets += len_synset
		mean_word_length += len(string)
		if len(string) > 0 and string[0].isupper(): num_capital_words += 1
		if string.isupper(): num_all_caps += 1
		#bag of words - unclean
		feats[string] = feats.get(string, 0) + 1

	feats['NUM_CAPITAL_WORDS'] = num_capital_words
	feats['NUM_ALL_CAPS'] = num_all_caps
	feats['NUM_EXCLAMATIONS_POINTS'] = num_exclamation_points
	feats['NUM_PUNCTUATION_MARKS'] = num_punctuation_marks
	feats['NUM_WORDS'] = num_words
	feats['MEAN_WORD_LENGTH'] = mean_word_length / float(num_words)
	feats['NUM_ELLIPSIS'] = num_ellipsis
	feats['NUM_LAUGH_WORDS'] = num_laugh_words
	# feats['NUM_EMOTICONS'] = num_emoticons
	feats['MEAN_SYNSETS'] = mean_synsets / float(num_words)
	feats['MAX_SYNSET'] = max_synset
	feats['SYNSET_GAP'] = max_synset - mean_synsets

	#bag of words, reply tweet
	for string in text2.split(' '):
		feats[string] = feats.get(string, 0) + 1




	return feats

def novel_phi(text1, time1, text2, time2):
	feats = {}
	for string in text1.split(' '):
		feats[string] = feats.get(string, 0) + 1

	return feats

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
	for text1, time1, text2, time2 in data:
		feat_dicts.append(phi(text1, time1, text2, time2))
		raw_examples.append(text1)
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

class Novel():
	def __init__(self):
		self.mod = LogisticRegression(fit_intercept = True)

	def train(self, X, Y):
		dataset = build_dataset(X, baseline_phi)
		self.mod.fit(dataset['X'], Y)
		self.vectorizer = dataset['vectorizer']

	def predict(self, X):
		dataset = build_dataset(X, novel_phi, vectorizer=self.vectorizer)
		return self.mod.predict(dataset['X'])

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

