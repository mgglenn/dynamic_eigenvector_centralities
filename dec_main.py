"""
Main implementation of "https://people.cs.clemson.edu/~isafro/papers/dynamic-centralities.pdf"

Grace Glenn (mgglenn@g.clemson.edu)
November 2017
"""
import argparse
import networkx as nx
from os import listdir
from os.path import isfile, join
import sys

# custom imports
import dec_text
import dec_graph


def get_files(file_folder='', file_format='file_%d.csv'):
	"""
	Return all interval files in a given folder.
	Usage:
		files = get_files('hourly_intervals/', 'file_%d.csv')
		# files = ['hourly_intervals/file_1.csv' ... 'hourly_inverals/file_216.csv']

	:param file_folder: where your files are
	:param file_format: how your files are named
	:returns files: ordered list of files to process.
	"""
	if len(file_folder):
		if file_folder[-1] != '/':
			file_folder += '/'
	
	num_files = len([f for f in listdir(file_folder) if isfile(join(file_folder, f))])

	files = []
	for i in range(0, num_files):
		files.append(file_folder + file_format % (i + 1))
		print(files[-1])

	return files


def build_args():
	"""
	Build out program arguments and return them.
	:returns: arguments pased by the user.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_folder",\
			    help="Location of the folder where your (numbered/ordered) interval files are.",\
			    type=str,\
			    default="intervals/")

	parser.add_argument("--output_folder", help="location of output files", type=str, default='dec_vals/')

	parser.add_argument("--P", help="Number of intervals to calculate DEC from.", type=int, default=5)

	parser.add_argument("--log_file", help="File to write output to.", type=str, default=None)
        
	# parser.add_argument("-v", "--verbosity", help="Prints various log messages", type=bool)

	return parser.parse_args()


def calculate_DEC(P=5, input_files=[], output_folder=''):
	"""
	Calculate DEC values on all text files.

	:param P: window of how many past ec values to use in slope (creating dec)
	:param files: (ORDERED) list of files to process, contains data
	"""
	G = nx.Graph()
	ec_windows = {}
	buckets = dec_graph.initialize_buckets(P=P)
	stopwords = dec_text.getStopwords()

	for interval, f in enumerate(input_files):
		print("Processing data from interval %d" % (interval + 1))

		# decrease edges, remove zero-weight edges and zero-degree nodes
		bucket_index = interval % P
		deleted = dec_graph.decrease_edge_weights_update_graph(G=G,\
					current_bucket=buckets[bucket_index],\
							ec_windows=ec_windows)

		# read in text from interval, update edge weights and node degrees 
		text = dec_text.get_text_from_file(file=f, stopwords=stopwords)
		dec_graph.update_graph_with_text(G=G,\
					    text=text,\
					    current_bucket=buckets[bucket_index])

		print("\tNum Keywords: %d" % len(G))

		# calculate DEC values and write them to file
		dec_vals = dec_graph.compute_dec_vals(G=G, ec_windows=ec_windows, P=P)

		outfile = output_folder + 'ecentrality%d.txt' % (interval + 1)
		dec_text.write_dec_values(outfile=outfile, dec_vals=dec_vals, rank=True)


if __name__ == "__main__":
	# argument parsing and some small format-checking
	args = build_args()

	if args.log_file:
	    sys.stdout = open(args.log_file, 'w')

	if len(args.output_folder):
		if args.output_folder[-1] != '/':
			args.output_folder += '/'
			print(args.output_folder)

	if len(args.input_folder):
		if args.input_folder[-1] != '/':
			args.input_folder += '/'
			print(args.input_folder)

	input_files = get_files(file_folder=args.input_folder)
	calculate_DEC(input_files=input_files, P=args.P, output_folder=args.output_folder)
