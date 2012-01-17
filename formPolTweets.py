#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
import toUnicode

class formPolTweets(object):

	def __init__(self, filetext):
		self.fileT = filetext
		self.train_filename = "data/allusers/train.txt"

	def parse(self):
		self.dataT = open(self.fileT)
		self.outFile = codecs.open(self.train_filename, 'w', 'utf-8')
	
		self.parse_data()

		self.dataT.close()
		self.outFile.close()

	
	def parse_data(self):
		counter = 0
		
		print( "Extracting informations from tweet file..." )
		
		for text_tweet in self.dataT:
			counter += 1
			if counter % 10000 == 0:
				print( "Read {0} lines.".format( counter) )
			
			#XXX non ha nessun senso convertire a unicode (filtrando eventuali codici html) se l'annotazione
			#e' gia' stata lanciata su questo file "sporco".. Al limite l'annotazione dovrebbe essere lanciata
			#dopo aver pulito il testo
			#text_tweet = toUnicode.toUnicode(text_tweet) 		#chiamo la funzione per convertire
			time, userID, text = text_tweet.split(None, 2) 		#None spezza sui caratteri bianchi

#4;;1880671990;;Fri May 22 02:04:47 PDT 2009;;NO_QUERY;;symbiancoder;;RT @jomtwi OMG LOL :D RT @tweetmeme One Step Forward, Nine Miles Back | untoldentertainment.com http://bit.ly/Lhqft				(esempio riga)
			
			self.outFile.write( unicode(" ;;{0};; ;; ;;{1};;{2}".format(time, userID, text), 'utf-8') )
	
		print( "Done." )		

if __name__ == '__main__':
	filetext = sys.argv[1]
	parser = formPolTweets(filetext)
	parser.parse()
