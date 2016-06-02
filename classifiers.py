from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer

def baseline_phi(text1, time1, text2, time2):
	feats = {}
	for string in text1.split(' '):
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

