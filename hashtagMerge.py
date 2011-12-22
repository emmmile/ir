#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs			


class tagMerge(object):

	def __init__(self, filename):
		self.filename = filename
		name, ext = os.path.splitext(filename)
		self.outFilename = name + ".hashtags"
		self.hashtags = dict()

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
				hashtag = t.split( None, 1 )[0]		#prende "tag"
				
				for pair in re.findall( '[\.\d]+ [^|]+', t ):	#itera sulle coppie "frequenza annotazione"
					couple = pair.split( None, 1 )
					an = couple[1]			#prende l'annotazione
					freq = int( couple[0] )	#prende la frequenza
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
			self.outFile.write( h )
			sortedAnnotations = sorted( self.hashtags[h].keys(), key=lambda x: -self.hashtags[h][x][1] )
			
			for a in sortedAnnotations:
				self.outFile.write( ' ' + a + ' f=' + str( self.hashtags[h][a][1] ) + ' u=' + str( self.hashtags[h][a][0] ) )

			self.outFile.write( '\n' )	



if __name__ == '__main__':
	filename = sys.argv[1]
	parser = tagMerge(filename)
	parser.parse()
