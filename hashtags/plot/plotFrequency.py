#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
#import toUnicode

class tagAnnotation(object):

	def __init__(self, filetext):
		self.fileT = filetext
		self.hashtags = dict()

	def parse(self):
		self.dataT = open(self.fileT)	
		self.parse_data()
		self.dataT.close()

	def print_data( self, dictionary, fileSuffix, keyPrefix, valuePrefix ):
		name, ext = os.path.splitext(self.fileT)
		out = open( name + fileSuffix, 'w')
		
		#stampo un file a due colonne (per gnuplot)
		#indice[TAB]score[\n]
		
		#out.write( "hashtag\tscore\n" )
		sortedHashtags = sorted( dictionary, key=lambda x: -dictionary[x][0] )
		for h in sortedHashtags:
			out.write( "{0}\t{1}\n".format( h, dictionary[h], len(dictionary[h][1]) ) )
		
		out.close()

	def parse_data(self):
		counter = 0
		
		print( "Extracting informations from tweet file..." )
		#hashtagAnn = dict()
		for text_tweet in self.dataT:
			counter += 1
			if counter % 10000 == 0:
				print( "Read {0} lines.".format( counter ) )
			
			#XXX non ha nessun senso convertire a unicode (filtrando eventuali codici html) se l'annotazione
			#e' gia' stata lanciata su questo file "sporco".. Al limite l'annotazione dovrebbe essere lanciata
			#dopo aver pulito il testo
			#text_tweet = toUnicode.toUnicode(text_tweet) 		#chiamo la funzione per convertire
			time, userID, text = text_tweet.split(None, 2) 		#None spezza sui caratteri bianchi
			tags = re.findall('#\w+', text.lower() )		#prendo gli hashtags
			tags = map( lambda y : y[1:], tags )			#toglie i cancelletti
			
			if len(tags) == 0:
				continue
			
			for t in tags :						#aggiungo le annotazioni nel dizionario
				if t in self.hashtags:
					self.hashtags[t] = [self.hashtags[t] + 1,self.hashtags[t][1]]
					self.hashtags[t][1].add(userID)
				else: 
					self.hashtags[t] = [1,set()]
					self.hashtags[t][1].add(userID)
			
		
		self.print_data( self.hashtags, ".plot", '', '' )	
		print( "Done." )	

if __name__ == '__main__':
	filetext = sys.argv[1]
	parser = tagAnnotation(filetext)
	parser.parse()
