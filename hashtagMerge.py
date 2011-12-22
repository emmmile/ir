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
		name, ext = os.path.splitext(filename)
		self.outFilename = name + ".hashtags"
		self.hashtags = dict()
		self.important = onlyImportant

	def parse(self):
		self.inFile = open(self.filename)
		self.outFile = open(self.outFilename, 'w')
	
		self.parse_data()

		self.inFile.close()
		self.outFile.close()

	def parse_data(self):
		print( "Merging hashtag informations from {0}...".format(self.filename) )
		for line in self.inFile:
			tags = line.split( ' #' )			#userID (#tag (frequenza annotazione)+)+
			for t in tags[1:]:				#toglie l'userID e itera su "tag (frequenza annotazione)+"
				tmp = t.split( None, 1 )
				hashtag = tmp[0]			#prende "tag"
				
				#for pair in re.findall( '[\.\d]+ [^|]+', tmp[1] ):	#itera sulle coppie "frequenza annotazione"
				for pair in tmp[1].split('|'):
					couple = pair.split( None, 1 )
					an = couple[1].rstrip()		#prende l'annotazione
					freq = int( couple[0] )		#prende la frequenza
					#freq = float( couple[0] )
					
					if hashtag not in self.hashtags:	#non esiste hashtag nel dizionario
						#il primo elemento della coppia e' il numero di utenti che ha usato
						#il tag "hashtag" con significato "an"
						#il secondo elemento invece e' il numero di tweet in cui compare
						#"hashtag" con il significato "an"
						self.hashtags[hashtag] = dict()
						self.hashtags[hashtag][an] = [1,freq]
					else:
						if an in self.hashtags[hashtag]:
							self.hashtags[hashtag][an][0] += 1
							self.hashtags[hashtag][an][1] += freq
						else:	self.hashtags[hashtag][an] = [1,freq]	#non esiste an per l'hashtag "hashtag"
	
		print( "Done.\nNow saving..." )
		self.print_data()
		print( "Saved." )
	
	def print_data(self):
		sortedHashtags = sorted( self.hashtags )
		for h in sortedHashtags:
			totalTweets = 0
			if self.important:
				for a in self.hashtags[h]:	# quante volte e' stato usato questo hashtag?
					totalTweets += self.hashtags[h][a][1]
			
			if self.important and totalTweets < 5000:	#continuo solo se e' stato usato almeno 10000 volte
				continue
			
			
			self.outFile.write( "#" + h.ljust(20) )
			# ordina le annotazioni in base al numero di utenti
			sortedAnnotations = sorted( self.hashtags[h].keys(), key=lambda x: -self.hashtags[h][x][0] )
			
			# stampo al massimo 20 annotazioni se important e' settato a True
			for a in sortedAnnotations[: (20 if self.important else len( sortedAnnotations ))]:
				self.outFile.write( ' ' + a + ' f=' + str( self.hashtags[h][a][1] ) + ' u=' + str( self.hashtags[h][a][0] ) )

			self.outFile.write( '\n' )	



if __name__ == '__main__':
	parser = OptionParser("Usage: ./hashtagMerge.py [options] FILE")
	parser.add_option('-o','--onlyimportant', action='store_true', default=False, help="flag used to print only most important tags.")
	(options, args) = parser.parse_args( sys.argv )
	if len( args ) != 2:
		parser.error( "Incorrect number of arguments." )
	
	tagger = tagMerge( args[1], options.onlyimportant )
	tagger.parse()

