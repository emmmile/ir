#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import json
import gzip
import codecs
import sys

try:
	import lzma
except ImportError:
	print( "No lzma module available. Please do not use .xz files." )



class TweetParser(object):
	
	def __init__(self, filename):
		self.filename = filename
		self.hashtags = dict()
	
	def add_hashtag_user( self, tag, userID, tweetID ):
		if tag not in self.hashtags:				# tag e' nuovo, quindi
			self.hashtags[tag] = dict()			# viene creato un nuovo map(utente, tweets)
			self.hashtags[tag][userID] = [tweetID]		# dove c'e' solo l'associazione (userID,tweetID)
		else:
			if userID in self.hashtags[tag]:
				self.hashtags[tag][userID].append(tweetID)
			else:	self.hashtags[tag][userID] = [tweetID]
	

	def extract_hashtags(self, juser):				# juser is a json object containing the tweets of the user
		userID = juser['user']
		for jtweet in juser['tweets']:				# get the tweets objects
			tweetID = jtweet['id_str']
			for jhashes in jtweet['entities']['hashtags']:	# get the hashtag objects
				#tag = jhashes['text']			# get the hashtag text (the hashtag)
				tag = jhashes['text'].lower()
				
				self.add_hashtag_user( tag, userID, tweetID )
	
	def parse(self):
		if self.filename[-3:] == ".xz":
			self.data = lzma.LZMAFile(self.filename)
		else:	self.data = open(self.filename)
			
		self.output = codecs.open(self.filename + '.hashtags.user', 'w', 'utf-8' )
		self.parse_data()
		self.data.close()
		self.output.close()

	def parse_data(self):
		counter = 0
		
		print( "Extracting hashtags from tweets..." )
		for tweets_to_write in self.data:
			self.extract_hashtags(json.loads(tweets_to_write))
			counter += 1
			if counter % 2000 == 0:
				print( "Read {0} lines. Dictionary size is {1}.".format( counter, len(self.hashtags) ) )
		
		print( "Done.\nNow sorting them and saving..." )
		sortedHashtags = sorted( self.hashtags.keys() ) #, key=str.lower )
		for h in sortedHashtags:
			sortedUsers = sorted( self.hashtags[h].keys() ) #ordina lessicograficamente
			tweets = ''
			for u in sortedUsers:
				tweets += " @" + str(u)
				if self.hashtags[h][u]:
					for ids in self.hashtags[h][u]:
						tweets += ' ' + str(ids)
				
			self.output.write( u"{0}{1}\n".format( h,tweets ) )
		print( "Done." )


if __name__ == '__main__':
    filename = sys.argv[1]
    parser = TweetParser(filename)
    parser.parse()

