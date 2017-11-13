"""
Text cleaning procedures implementation of 
"https://people.cs.clemson.edu/~isafro/papers/dynamic-centralities.pdf"

Grace Glenn (mgglenn@g.clemson.edu)
November 2017
"""
import csv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

def getStopwords(file='stopwords.txt'):
	"""
	Load in stop words.
	"""
	stopwordfile = open(file, 'r')
	stopwordlist = []
	for line in stopwordfile:
		for word in line.split():
			stopwordlist.append(word)
	return stopwordlist


def removeStopwords(text=[], stopwords=[]):
	"""
	Remove stopwords from a list of text.
	"""
	text = [x for x in text if x.lower() not in stopwords]
	text = [x for x in text if len(x) > 1]
	return text


def stemText(text=[]):
	"""
	Stem text.
	"""
	wordnet_lemmatizer = WordNetLemmatizer()
	stemmed = []
	for word in text:
		stemmed.append(wordnet_lemmatizer.lemmatize(word))
	return stemmed


def removeHashTag(text=[]):
	"""
	Remove hashtag form givne set of words.
	"""
	cleanedText = []
	for word in text:
		word = word.replace("#","")
		cleanedText.append(word)
	return cleanedText


def preprocessKeywords(text=[], stopwords=[]):
	"""
	Process all tokens.
	:param text: word tokens representing a document (ie tweet).
	:param stopwords: stopwords to filter on.
	:returns text: cleaned text
	"""
	text = removeHashTag(text)
	text = stemText(text)
	text = removeStopwords(text, stopwords=stopwords)
	return text


def getWords(text):
	"""
	Remove some speical characters and hyperlinks from text.
	:param text: string representing a tweet
	:returns words: cleaned tokens.
	"""
	text = re.sub("<.*?>","",text.lower())
	text = re.sub(r"http\S+", "", text)
	words = re.compile(r'[^A-Z^a-z]+').split(text)
	return words


def get_text_from_file(file=None, stopwords=[]):
	"""
	Takes all tweets from a given file and returns data, list of all keyword lists.
	:param file: file to process
	:returns data: list of lists

	eg
	# data[0] = ['boston', 'marathon', 'broadcast', 'live']
	"""
	data = []
	with open(file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for line in reader:
			tweetData = line[1]
			tweet = getWords(tweetData)
			tweetKeywords = preprocessKeywords(tweet, stopwords=stopwords)

			# make sure we have at least one pair (edge)
			if len(tweetKeywords) > 1:
				data.append(tweetKeywords)
	return data


def write_dec_values(outfile='', dec_vals=None, rank=False):
	"""
	Writes dynamic ecentrality values to a given file.
	:param outfile: file to write to
	:param dec_vals: dictionary of word->dec pairs
	:returns: number of keywords read
	"""
	items = dec_vals.items()

	if rank:
		# arrange keywords from highest to lowest DEC value
		items = sorted(items, key=lambda x: x[1], reverse=True)
		samp = items[:5]
		print("\tTop five keywords: ")
		for pair in samp:
			print("\t\t" + str(pair))

	keywords = 0
	ecentral = open(outfile,'w')
	for word, dec in items:
		ecentral.write(word)
		ecentral.write(" ")
		ecentral.write(str(dec))
		ecentral.write('\n')
		keywords += 1

	return keywords
