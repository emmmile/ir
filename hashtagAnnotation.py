#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
import toUnicode

class tagAnnotation(object):

	def __init__(self, filetext, fileannotation):
		self.fileT = filetext
		self.fileA = fileannotation
		name, ext = os.path.splitext(filetext)
		self.hashtag_filename = name + ".hashtagsUser"

	def parse(self):
		self.dataT = open(self.fileT)
		self.dataA = open(self.fileA)
		self.outFile = codecs.open(self.hashtag_filename, 'w', 'utf-8')
	
		self.parse_data()

		self.dataA.close()
		self.dataT.close()
		self.outFile.close()

	def printLine(self, userID_old, hashtagAnn ):
		#calcola la lunghezza totale delle annotazioni, cioe' guarda se il dizionario hashtagAnn
		#che e' riferito a userID_old, contiene almeno un elemento
		total = 0
		total = map( lambda x: total + len(hashtagAnn[x]), hashtagAnn )
		
		#if len( hashtagAnn ) and total:
		if total == 0:
			return
		
		self.outFile.write(userID_old)
		for t in hashtagAnn:				# scorre i tag dell'utente
			if len( hashtagAnn[t] ):		# se ci sono annotazioni...
				result = dict()			# creo un dizionario che ha annotazioni come chiavi
								# e numero di tweet come valori
				for a in hashtagAnn[t]:
					#key, rho = a.split('@')
					#result[key] = result.setdefault( key, 0.0 ) + float(rho)
					result[a] = result.setdefault( a, 0 ) + 1
					#if a == "Quore":
					#	print( result[a] )
								# sommo 1 se trovo l'annotazione a
				
				resultList = []
				for el in result:		# scorro il dizionario e creo una lista
								# di stringhe "frequenza annotazione" che poi viene scritto su file
					resultList.append( str( result[el] ) + ' ' + el )
				
				#ogli coppia "frequenza annotazione" e' separata da |
				self.outFile.write( unicode(" {0} {1}".format(t, '|'.join( resultList ) ), 'utf-8') )
		self.outFile.write("\n")


	def parse_data(self):
		counter = 0
		
		print( "Extracting informations from tweet file..." )
		userID_old = ""
		#hashtagAnn = dict()
		for text_tweet in self.dataT:
			annotation_tweet = self.dataA.readline()
			counter += 1
			if counter % 10000 == 0:
				print( "Read {0} lines (current user: {1}).".format( counter, userID_old ) )
			
			#XXX non ha nessun senso convertire a unicode (filtrando eventuali codici html) se l'annotazione
			#e' gia' stata lanciata su questo file "sporco".. Al limite l'annotazione dovrebbe essere lanciata
			#dopo aver pulito il testo
			#text_tweet = toUnicode.toUnicode(text_tweet) 		#chiamo la funzione per convertire
			time, userID, text = text_tweet.split(None, 2) 		#None spezza sui caratteri bianchi
			tags = re.findall('#\w+', text.lower() )		#prendo gli hashtags
			
			if len(tags) == 0 :
				continue
				
			#annotations = re.findall('#[@\w\.]+', annotation_tweet)	#prende le annotazioni
			annotations = re.findall('#[^#]+', annotation_tweet.rstrip() )

			annotations = map( lambda x: x[1:], annotations )	#toglie magicamente il cancelletto
			if userID_old == "":					#controlla se e' la prima iterazione
				hashtagAnn = dict()
				userID_old = userID
			if userID_old != userID :				#se ho finito il blocco di un utente
				self.printLine( userID_old, hashtagAnn )	#stampo sul file
				hashtagAnn = dict()				#inizializzo un nuovo dizionario...
				userID_old = userID				#...per il nuovo utente
			
			if len(annotations) == 0:
				continue
			
			for t in tags :						#aggiungo le annotazioni nel dizionario
				if t in hashtagAnn:
					hashtagAnn[t] = hashtagAnn[t] + annotations
				else: 	hashtagAnn[t] = annotations
				
			if len( annotations ) == 32768:
				print( annotation_tweet )
		print( "Done." )		

if __name__ == '__main__':
	filetext = sys.argv[1]
	fileannotation = sys.argv[2]
	parser = tagAnnotation(filetext,fileannotation)
	parser.parse()
