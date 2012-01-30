#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
from optparse import OptionParser #deprecated in 2.7 or newer


class tagMerge(object):

	def __init__(self, filename, onlyImportant):
		self.filename = filename
		self.hashtags = dict()		# mapping hashtag -> topics
		self.topics = dict()		# mapping topic -> hashtags
		self.important = onlyImportant
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
					freq = int( couple[0] )		#prende la frequenza
					#freq = float( couple[0] )
					self.totalTweets += freq
					
					if hashtag not in self.hashtags:	#non esiste hashtag nel dizionario
						#il primo elemento della coppia e' il numero di utenti che ha usato
						#il tag "hashtag" con significato "an"
						#il secondo elemento invece e' il numero di tweet in cui compare
						#"hashtag" con il significato "an"
						self.hashtags[hashtag] = dict()
						self.hashtags[hashtag][an] = math.log(freq)
					else:
						if an in self.hashtags[hashtag]:
							self.hashtags[hashtag][an] += math.log(freq)
						else:	self.hashtags[hashtag][an] = math.log(freq)	#non esiste an per l'hashtag "hashtag"
	
		print( "Done [total users: {0}, total tweets: {1}].\nNow inverting...".format( self.totalUsers, self.totalTweets ) )
		self.invert()
		print( "Inverted [total topics: {0}].\nNow saving...".format( len( self.topics ) ) )
		self.print_data( self.hashtags, ".hashtags", '#', '' )
		self.print_data( self.topics, ".topics", '', '#' )
	
	def invert( self ):
		for h in self.hashtags:				# scorro gli hashtags
			for t in self.hashtags[h]:		# scorro i topic e gli aggiungo al dizionario
				# ad ogni topic viene associato un dizionario di hashtags.
				# ad ogni hashtag vengono associate le stesse informazioni di prima (utenti/frequenza)
				if t not in self.topics:
					self.topics[t] = dict()
					self.topics[t][h] = self.hashtags[h][t]
				else:
					if h in self.topics[t]:
						self.topics[t][h] += self.hashtags[h][t]
					else:
						self.topics[t][h] = self.hashtags[h][t]
	
	
	
	def print_data( self, dictionary, fileSuffix, keyPrefix, valuePrefix ):
		name, ext = os.path.splitext(self.filename)
		out = open( name + fileSuffix, 'w')
		
		sortedHashtags = sorted( dictionary )
		for h in sortedHashtags:
			
			out.write( keyPrefix + h )
			# ordina le annotazioni in base al numero di utenti
			sortedAnnotations = sorted( dictionary[h].keys(), key=lambda x: -dictionary[h][x] )
			
			printed = 0
			# stampo le annotazioni fino a quando non ho considerato il 60% dei tweets
			for a in sortedAnnotations:
				out.write( ' ' + valuePrefix + a + ' s=' + str( dictionary[h][a] ) )
				if self.important:
					printed += 1
					if printed >= 20
						break

			out.write( '\n' )
		
		out.close()


if __name__ == '__main__':
	parser = OptionParser("Usage: ./hashtagMerge.py [options] FILE")
	parser.add_option('-o','--onlyimportant', action='store_true', default=False, help="flag used to print only most important topics (and tags).")
	(options, args) = parser.parse_args( sys.argv )
	if len( args ) != 2:
		parser.error( "Incorrect number of arguments." )
	
	tagger = tagMerge( args[1], options.onlyimportant )
	tagger.parse()

