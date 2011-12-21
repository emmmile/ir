#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys		
import gzip
import os
import codecs


if __name__ == '__main__':
	tweets_file = open( sys.argv[1] ) #
	annotation_file = open( sys.argv[2] ) #
	name, ext = os.path.splitext(sys.argv[1])
	new_filename = name + ".newTweets"
	new_tweets_file = codecs.open(new_filename, 'w', 'utf-8')
	
	for aLine in annotation_file:
	
		stime, suser, stext = aLine.split( None, 2 )
		if stime == "1311583139" and suser == "1491213017919":
			continue

		
		while True:			
			tline = tweets_file.readline()
			if tline == "":
				sys.stderr.write("Attenzione: tweet per annotazione non trovato!\n")
				sys.stderr.write(aLine)
				sys.exit()
			
			try:
				ftime, fuser, ftext = tline.split( '\t', 2 )
			except ValueError:
				print(tline)
		
			if ftime == stime and fuser == suser:
				new_tweets_file.write(unicode(tline,'utf-8'))
				break
	new_tweets_file.close()
	tweets_file.close()
	annotation_file.close()
