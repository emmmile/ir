#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
from optparse import OptionParser #deprecated in 2.7 or newer
import math

class tagPrint(object):

	def __init__(self, filename, onlyImportant,threshold):
		self.filename = filename
		self.hashtags = dict()		# mapping hashtag -> topics
		self.important = onlyImportant
		self.threshold = threshold
		self.totalUsers = 0
		self.totalTweets = 0

	def parse(self):
		self.inFile = open(self.filename)
		self.parse_data()
		self.inFile.close()

	def parse_data(self):
		print( "Merging hashtag informations from {0}...".format(self.filename) )
		for line in self.inFile:
			tags = line.split( ' #' )			#userID (#tag (frequenza annotazione)+)+
			self.totalUsers += 1
			
			for t in tags[1:]:				#toglie l'userID e itera su "tag (frequenza annotazione)+"
				tmp = t.split( None, 1 )
				hashtag = tmp[0]			#prende "tag"
				
				#for pair in re.findall( '[\.\d]+ [^|]+', tmp[1] ):	#itera sulle coppie "frequenza annotazione"
				for pair in tmp[1].split('|'):
					couple = pair.split( None, 1 )
					an = couple[1].rstrip()		#prende l'annotazione
					#freq = int( couple[0] )	#XXX prende la frequenza nel caso sia un int
					freq = float( couple[0] )	#XXX nel caso sia un float (somma dei rho)
					self.totalTweets += freq
					
					if hashtag not in self.hashtags:	#non esiste hashtag nel dizionario
						#il primo elemento della coppia e' il numero di utenti che ha usato
						#il tag "hashtag" con significato "an"
						#il secondo elemento invece e' il numero di tweet in cui compare
						#"hashtag" con il significato "an"
						self.hashtags[hashtag] = dict()
						self.hashtags[hashtag] = freq
					else:
						self.hashtags[hashtag] += freq
	
		print( "Done [total users: {0}, total tweets (or score): {1}].\n".format( self.totalUsers, self.totalTweets ) )
		self.print_data( self.hashtags, ".plot", '', '' )
	
	
	def print_data( self, dictionary, fileSuffix, keyPrefix, valuePrefix ):
		name, ext = os.path.splitext(self.filename)
		out = open( name + fileSuffix, 'w')
		
		#stampo un file a due colonne (per gnuplot)
		#indice[TAB]score[\n]
		
		#out.write( "hashtag\tscore\n" )
		index = 0
		sortedHashtags = sorted( dictionary, key=lambda x: -dictionary[x] )
		for h in sortedHashtags:
			out.write( "{0}\t{1}\n".format( index, dictionary[h] ) )
			index += 1
		
		out.close()


if __name__ == '__main__':
	parser = OptionParser("Usage: ./hashtagMerge.py [options] FILE")
	parser.add_option('-o','--onlyimportant', action='store_true', default=False, help="flag used to print only most important topics (and tags).")
	parser.add_option('-t','--threshold', action='store',type='float',dest='threshold',help="set the threshold value for printing (% of the total users). Use with -o.")
	(options, args) = parser.parse_args( sys.argv )
	if len( args ) != 2:
		parser.error( "Incorrect number of arguments." )
	
	tagger = tagPrint( args[1], options.onlyimportant, options.threshold )
	tagger.parse()

