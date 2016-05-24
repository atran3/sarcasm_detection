from sklearn.linear_model import LogisticRegression

def baseline_phi(time1, time2, text1, text2):
	feats = {}
	for string in array:
		feats[string] = feats.get(string, 0) + 1

	return feats

def binary_class_func(y):
	if y == 0:
		return "neutral"
	else if y == 1:
		return "sarcastic"
	else:
		return None

def build_dataset(reader, phi, class_label, vectorizer=None):
	labels = []
    feat_dicts = []
    raw_examples = []
    for time1, time2, text1, text2 in reader():
        labels.append(class_label)
        feat_dicts.append(phi(time1, time2, text1, text2))
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
            'y': labels, 
            'vectorizer': vectorizer, 
            'raw_examples': raw_examples}


# Logistic Regression on bag of words
class Baseline():
	def __init__(self):
		self.mod = LogisticRegression(fit_intercept = True)

	def train(self, X, Y):
		self.mod.fit(X,Y)

	def predict(self, X):
		return self.mod.predict(X)
