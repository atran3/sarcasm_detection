from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import bigrams
import re
import sys
import json

FILES = ["educationCleanData.csv", "ironyCleanData.csv", "newspaperCleanData.csv", "politicsCleanData.csv", "humourCleanData.csv", "sarcasmCleanData.csv"]

def getNGramFeatures(feats, text, prefix):
	for string in text.lower().split(' '):
		feats[prefix + string] = feats.get(string, 0) + 1
	for bigram in bigrams(text.lower().split(' ')):
		feats[prefix + ' '.join(bigram)] = feats.get(' '.join(bigram), 0) + 1

def getLaughFeatures(feats, text, prefix):
	feats[prefix + 'NUM_LAUGH_WORDS'] = len(re.findall(r'lol|haha|hahaha|rofl|lmao', text))
	feats[prefix + 'NUM_EMOTICONS'] = len(re.findall(r'\:\)|\:\(|\;\)|\:D', text))

def getWordFeatures(feats, text, prefix):
	num_words = len(text.split(' '))
	min_word_length = sys.maxint
	max_word_length = 0
	mean_word_length = 0
	mean_synsets = 0
	max_synset = 0

	for string in text.lower().split(' '):
		if len(string) > 0 and string[0] == '#':
			string = string[1:]
		len_synset = len(wn.synsets(string))
		if len_synset > max_synset: max_synset = len_synset
		mean_synsets += len_synset
		mean_word_length += len(string)
		if len(string) > max_word_length:
			max_word_length = len(string)
		if len(string) < min_word_length:
			min_word_length = len(string)

	feats[prefix + 'MEAN_SYNSETS'] = mean_synsets / float(num_words)
	feats[prefix + 'MAX_SYNSET'] = max_synset
	feats[prefix + 'SYNSET_GAP'] = max_synset - mean_synsets
	feats[prefix + 'NUM_WORDS'] = num_words
	feats[prefix + 'MEAN_WORD_LENGTH'] = mean_word_length / float(num_words)
	feats[prefix + 'MIN_WORD_LENGTH'] = min_word_length
	feats[prefix + 'MAX_WORD_LENGTH'] = max_word_length

def getSentimentFeatures(feats, text, prefix):
	pos_sum = 0
	neg_sum = 0
	most_positive = 0
	most_negative = 0

	for string in text.lower().split(' '):
		if len(string) > 0 and string[0] == '#':
			string = string[1:]
		senti_synset = list(swn.senti_synsets(string))
		if len(senti_synset) > 0:
			senti_synset = senti_synset[0] #just use the 1st one for now
			pos_score = senti_synset.pos_score()
			if pos_score > most_positive: most_positive = pos_score
			pos_sum += pos_score
			neg_score = senti_synset.neg_score()
			if neg_score > most_negative: most_negative = neg_score
			neg_sum += neg_score

	feats[prefix + 'POS_SUM'] = pos_sum
	feats[prefix + 'NEG_SUM'] = neg_sum
	feats[prefix + 'MEAN_POS_NEG'] = (pos_sum + neg_sum) / 2.0
	feats[prefix + 'POS_NEG_GAP'] = pos_sum - neg_sum
	feats[prefix + 'SINGLE_POS_GAP'] = most_positive - (pos_sum + neg_sum) / 2.0
	feats[prefix + 'SINGLE_NEG_GAP'] = most_negative - (pos_sum + neg_sum) / 2.0

def getPunctuationFeatures(feats, text, prefix):
	feats[prefix + 'NUM_EXCLAMATIONS_POINTS'] = len([1 for ch in text if ch == '!'])
	feats[prefix + 'NUM_PUNCTUATION_MARKS'] = len([1 for ch in text if ch in ['!', ',', '.', '?', '"', ';', '-']])
	feats[prefix + 'NUM_ELLIPSIS'] = len(re.findall(r'\.\.\.', text))
	feats[prefix + 'NUM_HASHTAGS'] = len([1 for ch in text if ch == '#'])

def featurize(infile, outfile, category):
	counter = 0
	all_features = []
	with open(infile, 'r') as inf:
		reader = inf.read().split('\x1E')
		for example in reader:
			features = dict()
			example = example.split('\x1F')
			if len(example) <= 1: continue
			features['TEXT'] = example[0]
			features['TEXT_TIME'] = example[1]
			getPunctuationFeatures(features, example[0], '')
			getSentimentFeatures(features, example[0], '')
			getWordFeatures(features, example[0], '')
			getLaughFeatures(features, example[0], '')
			getNGramFeatures(features, example[0], '')
			if example[2] != '':
				features['REPLY_TEXT'] = example[2]
				features['REPLY_TIME'] = example[3]
				getPunctuationFeatures(features, example[2], 'REPLY_')
				getSentimentFeatures(features, example[2], 'REPLY_')
				getWordFeatures(features, example[2], 'REPLY_')
				getLaughFeatures(features, example[2], 'REPLY_')
				getNGramFeatures(features, example[2], 'REPLY_')
			all_features.append(features)
			counter += 1
			print "successfully read" + str(counter) + "tweets!!"
		json.dump(all_features, outfile)

def main():
	global FILES
	for infile in FILES:
		category = infile.split('CleanData')[0]
		with open(category + "Featurized.csv", 'w') as outfile:
			featurize(infile, outfile, category)
			print "finished" + infile + "!"

if __name__ == "__main__":
    main()
