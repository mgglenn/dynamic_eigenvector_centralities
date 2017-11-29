import datetime
import json
import time
import csv
import argparse

def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval",\
			help="time interval to break tweets by", \
			type=int,\
			default=60)

    parser.add_argument("--input_file",\
			help="raw input file",\
			type=str,\
			default="/scratch2/mgglenn/boston/sorted.csv")

    parser.add_argument("--output_folder",\
			help="output folder to output files to",\
			type=str,\
			default="/scratch2/mgglenn/boston/intervals/int/")

    return parser.parse_args()


if __name__ == "__main__":
    args = build_args()
    
    i=0
    phr=''
    pday=''
    pmin=0
    interval_len = args.interval
    interval = -1

    with open(args.input_file, 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
	    tId = line[2]; #tweet_long.partition(',')[2]
	    tweetText = line[1]
	    tDate = line[0]
	    tweetDate = datetime.datetime.strptime(tDate, "%Y-%m-%d %H:%M:%S-04:00")
	    day=tweetDate.day
	    hr=tweetDate.hour
	    minute=tweetDate.minute
	    curr_interval = minute / interval_len

	    break_file = False
	    if interval_len == 60:
		break_file = (i is 0 or hr is not phr)
	    else:
		break_file = (i is 0 or curr_interval != interval)

	    if break_file:
		interval = curr_interval
		pmin = minute
		phr = hr
		print(str(tweetDate)) 
		i = i+1
		csvfile2 = open(args.output_folder + "/file_" + str(i)+".csv",'wb')
		f1 = csv.writer(csvfile2, delimiter=',')

	    f1.writerow(line)
