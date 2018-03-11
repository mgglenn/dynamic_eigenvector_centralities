"""
Graph algorithms and implementation of 
"https://people.cs.clemson.edu/~isafro/papers/dynamic-centralities.pdf"

Grace Glenn (mgglenn@g.clemson.edu)
November 2017
"""
from collections import deque
from scipy import stats
import networkx as nx
import numpy as np


def decrease_edge_weights_update_graph(G=None, current_bucket=None, ec_windows=None):
	"""
	Take all the edge->weight pairs in current_bucket and use them
	to decrement the edges in G, and remove edges with weight 0 or 
	nodes with degree 0.

	:param G: graph
	:param current_bucket: a dictionary of edge->weight counts we'll
	use to decrement the edge->weight pairs in G.
	:param ec_windows: a dictionary containing the last "P" eigenvector centrality
	measures we use for computing DEC values. If we delete a node from the Graph
	we'll delete it from our windows, too.

	:returns: deleted_words, the list of words we removed
	"""
	deleted_words = []
	for edge, bucket_weight in current_bucket.items():
		# get words from edge
		word1, word2 = edge.split(',')
		G[word1][word2]['weight']-=bucket_weight

		if G[word1][word2]['weight'] <= 0:
			G.remove_edge(word1,word2)

		# remove nodes with no degrees from graph and ec_windows
		if G.degree(word1) == 0:
			deleted_words.append(word1)
			G.remove_node(word1)
			del ec_windows[word1]

		if G.degree(word2) == 0:
			deleted_words.append(word2)
			G.remove_node(word2)
			del ec_windows[word2]

	# clear weights from bucket
	current_bucket.clear()
	return deleted_words


def update_graph_with_text(G=None, text=[], current_bucket=None):
	"""
	Take a graph, G, and for each tweet in text, update pairs.
	:param G: current Graph object
	:param text: list of tweets
	:param current_bucket: the dictonary for tracking co-occurences.
	:returns: None, just updates bucket and graph.
	"""
	for tweet_words in text:
		for i in range(0, len(tweet_words)):
			for j in range(i, len(tweet_words)):
				word1 = tweet_words[i]
				word2 = tweet_words[j]
				edge = update_graph_with_edge(G=G, word1=word1, word2=word2)

				# count number of times the edge appears
				if edge in current_bucket:
					current_bucket[edge] += 1
				else:
					current_bucket[edge] = 1


def update_graph_with_edge(G=None, word1='', word2=''):
	"""
	Simply make sure our edges our alphabetized. Then increment
	the weight on the Graph.
	:param word1: one word in your edge
	:param word2: other word
	:param G: graph to update
	:returns edge:
	"""
	if word1 < word2:
		edge = word1 + "," + word2
	else:
		edge = word2 + "," + word1

	u, v = edge.split(',')
	G.add_node(u)
	G.add_node(v)
	if G.has_edge(u,v):
		G[u][v]['weight'] += 1
	else:
		G.add_edge(u, v)
		G[u][v]['weight'] = 1

	return edge


def initialize_buckets(P=5):
	buckets = []
	for i in range(0, P):
		buckets.append({})
	return buckets


def update_ec_windows(G=None, ec_windows=None, P=5, weight='weight', normalize=True):
	"""
	We calculate dynamic ec's by using the last P ec values.
	:param G: graph
	:param ec_windows: a dictionary with the last P ec values for each word
	:param weight:
	:param normalize: 
	:returns ecentrality, the current ecentrality for each word
	:side effect: updates ec_windows with most recent P values.
	"""
	ecentrality = nx.eigenvector_centrality(G, weight=weight)

	if normalize:
		maxKey = max(ecentrality , key=ecentrality.get)
		maxC = ecentrality[maxKey]
		for key in ecentrality:
			ecentrality[key] = ecentrality[key] / maxC

	for word, ec_val in ecentrality.items():
		window = ec_windows.setdefault(word, deque())
		if len(window)>=P-1:
			window.popleft()
		window.append(ecentrality[word])
		ec_windows[word] = window

	return ecentrality


def calculate_slope(x, y):
	"""
	Simply calculates linear slope (a bit leaner than the library implementation).
	"""
        try:
            x_hat = np.average(x)
            y_hat = np.average(y)

            y_diff = [yi - y_hat for yi in y]
            x_diff = [xi - x_hat for xi in x]

            num = np.dot(x_diff, y_diff)
            denom = np.dot(x_diff, x_diff)
            slope = num / denom
            return slope
        except:
            return 0


def compute_dec_vals(G=None, ec_windows=None, P=5):
	"""
	:param G: current graph
	:param ec_windows: a list of the last P ec_vals for each word
	:param P: the length of your window
	:returns ec_vals: dynaimc eigenvector centralities for each word.
	"""
	# update the ec_windows with eigenvector centrality
	ec_vals = update_ec_windows(G=G, ec_windows=ec_windows, P=P)

	for word, y in ec_windows.items():
		x = [i+1 for i in range(0, len(y))]
		slope = 0
		if len(y)>1:
			slope = calculate_slope(x, y)
			# slope, intercept, r_value, pvalue, std_err = stats.linregress(x,y)

		# make the ec_value dynamic
		ec_vals[word]*=slope

	return ec_vals
