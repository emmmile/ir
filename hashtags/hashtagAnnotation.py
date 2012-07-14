#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
import toUnicode


"""
INPUT:
  A file containing the tweets in the following format:		time[BLANK]userID[BLANK]textWithHashtags[NEWLINE]
  For example (data/i3terroni-dataset/with-hashtags):
  
  1323335672	99997947	[Me ne frego io!!] Solo a Roma 10mila testamenti a favore di Cazzinger #dilloamonti #ICI
  1323336521	99997947	#APSA protegge il Mattone di Dio! Al catasto molti mattoni non risultano... #dilloamonti #ICI
  1323336802	99997947	Leggi un dossier sulla Chiesa e ti dai l'estrema unzione da solo! Amen #dilloamonti
  ...
  
  The same annotated file, with format:				time[BLANK]userID[BLANK]#annotation@score...[NEWLINE]
  For example (data/i3terroni-dataset/with-hashtags.annotations):
  1323335672	99997947	#Roma@0.44241688
  1323336521	99997947	#Catasto@0.29792827#Dio@0.20322153#Mattone@0.28075898#Mattone@0.27452058
  1323336802	99997947	#Unzione degli infermi@0.55601376
  ...
  
  
  
OUTPUT:
  A file with the following format:				userID[BLANK](#hashtag[BLANK]score[BLANK]annotationID...)...[NEWLINE]
  For example (data/i3terroni-dataset/with-hashtags.hashtagUser):
  
  100110609 #whatsapp 0.4090909 1 Televideo|0.36914182 1 Apple|0.61621785 1 IPhone (famiglia) #pid 0.5399709 1 Il Popolo della Libertà
  ...
  
  This file has to be used as input for hashtagMerge.py, and it is saved in the same directory of the two input files.
"""

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
				resultRhos = dict()		# creo un dizionario che ha annotazioni come chiavi
								# e numero di tweet come valori
				resultFreq = dict()
				
				for a in hashtagAnn[t]:
					#XXX questo e' da usare nel caso il file annotato contenga anche il rho
					key, rho = a.split('@')
					resultRhos[key] = resultRhos.setdefault( key, 0.0 ) + float(rho)
					#XXX altrimenti basta questa riga
					resultFreq[key] = resultFreq.setdefault( key, 0 ) + 1
				
				toPrint = []			# questo contiene una rappresentazione testuale
								# delle sommeRho e delle frequenze di tutte le annotazioni
								# relative all'hashtag corrente, t
				
				for el in resultRhos:		# scorro il dizionario (uno vale l'altro) e creo una lista
								# di stringhe "frequenza annotazione" che poi viene scritto su file
					toPrint.append( str( resultRhos[el] ) + ' ' + str( resultFreq[el] ) + ' ' + el )
					
				
				#ogli coppia "sumRho frequenza annotazione" e' separata da |
				self.outFile.write( unicode(" {0} {1}".format(t, '|'.join( toPrint ) ), 'utf-8') )
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
			
			if len(tags) == 0:
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
