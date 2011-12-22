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
	new_filename = name + ".filtered"
	new_tweets_file = codecs.open(new_filename, 'w', 'utf-8')
	counter = 0
	
	print( "Filtering tweets based on annotations (tweets with no annotation will be discarded)..." )
	for aLine in annotation_file:
		stime, suser, stext = aLine.split( None, 2 )
		counter += 1
		if counter % 100000 == 0:
			print( "Read {0} annotated lines.".format( counter ) )
		
		while True:			
			tline = tweets_file.readline()
			if tline == "":
				print( "ATTENTION: no tweet found for annotation \'{0}\'.".format( aLine ) )
				sys.exit()
			
			#try:
			ftime, fuser, ftext = tline.split( '\t', 2 )
			#except ValueError:
			#	print(tline)
		
			if ftime == stime and fuser == suser:
				new_tweets_file.write(unicode(tline,'utf-8'))
				break
	
	print( "Done." )
	new_tweets_file.close()
	tweets_file.close()
	annotation_file.close()
