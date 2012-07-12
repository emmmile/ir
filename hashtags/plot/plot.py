#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
from optparse import OptionParser #deprecated in 2.7 or newer
import math



"""
INPUT:
  A file containing the hashtag annotation informations as explained in hashtagAnnotation.py.  
  
OUTPUT:
  A table with the following format:		rank[BLANK]users[BLANK]score[BLANK]frequency[BLANK]hashtag[BLANK]annotation[NEWLINE]
  
"""



class plotMerge(object):

	def __init__(self, filename):
		self.filename = filename
		self.hashtags = dict()		# mapping hashtag -> topics
		self.totalUsers = 0
		self.totalTweets = 0

	def parse(self):
		self.inFile = open(self.filename)
		self.print_plot()
		self.inFile.close()

	def print_plot(self):
		print( "Printing hashtag informations from {0}...".format(self.filename) )
		for line in self.inFile:
			tags = line.split( ' #' )			#userID (#tag (frequenza annotazione)+)+
			self.totalUsers += 1
			
			for t in tags[1:]:				#toglie l'userID e itera su "tag (frequenza annotazione)+"
				tmp = t.split( None, 1 )
				hashtag = tmp[0]			#prende "tag"
				
				
				for triple in tmp[1].split('|'):
					fields = triple.split( None, 2 )
					an = fields[2].rstrip()		#prende l'annotazione
					freq = int( fields[1] )		#prende la frequenza
					rhos = float( fields[0] )	#prende la somma dei rhos
					self.totalTweets += freq
					
					if hashtag not in self.hashtags:
						self.hashtags[hashtag] = dict()
						self.hashtags[hashtag][an] = (1,math.log(1 + freq,2),freq)
					else:
						if an in self.hashtags[hashtag]:
							self.hashtags[hashtag][an] = (self.hashtags[hashtag][an][0] + 1,
										      self.hashtags[hashtag][an][1] + math.log(1 + freq,2),
										      self.hashtags[hashtag][an][2] + freq)
						else:	self.hashtags[hashtag][an] = (1,math.log(1 + freq,2),freq)	
						
		print( "Done [total users: {0}, total tweets: {1}].\n".format( self.totalUsers, self.totalTweets ) )
		
		allPairs = []
		for h in self.hashtags:
			for a in self.hashtags[h]:
				allPairs.append( (h,a) )
		
		
		rank = 1
		out = open( "frequency-score-users.plot", 'w')
		#out.write( "rank\tusers\tscore\tfrequency\thashtag\tannotation\n" )
		out.write( "rank\tusers\tscore\tfrequency\thashtag\n" )
		sortedPairs = sorted( allPairs, key=lambda x: -self.hashtags[x[0]][x[1]][1] )		#ordino sulla frequenza, x e' una coppia
		for p in sortedPairs:
			h = p[0]
			a = p[1]
			#out.write( "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format( rank, self.hashtags[h][a][0], 
			#	   self.hashtags[h][a][1], self.hashtags[h][a][2], h, a ) )
			out.write( "{0}\t{1}\t{2}\t{3}\t{4}\n".format( rank, self.hashtags[h][a][0], 
				   self.hashtags[h][a][1], self.hashtags[h][a][2], h ) )
			
			rank += 1
		out.close()
		
		


if __name__ == '__main__':
	if len( sys.argv ) != 2:
		print( "Incorrect number of arguments." )
		exit()

	tagger = plotMerge( sys.argv[1] )
	tagger.parse()

