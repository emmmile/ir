#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-


import json
import gzip
import codecs
import re
import os
import time
import sys

"""
Creates the 3 files list, text and hashtags from the json tweet file. I think is no more necessary.
"""


try:
	import lzma
except ImportError:
	print( "No lzma module available. Please do not use .xz files." )


class TweetParser(object):

	def __init__(self, filename):
		self.filename = filename
		name, ext = os.path.splitext(self.filename)
		self.list_filename = name + ".list"
		self.text_filename = name + ".text"
		self.hash_filename = name + ".hashtags"
		self.tweet_set = set()
		self.hashtags = dict()
        
	def add_hashtag_user( self, tag, userID, tweetID ):
		if tag not in self.hashtags:				# tag e' nuovo, quindi
			self.hashtags[tag] = dict()			# viene creato un nuovo map(utente, tweets)
			self.hashtags[tag][userID] = [tweetID]		# dove c'e' solo l'associazione (userID,tweetID)
		else:
			if userID in self.hashtags[tag]:
				self.hashtags[tag][userID].append(tweetID)
			else:	self.hashtags[tag][userID] = [tweetID]
	

	def parse_user(self, juser):					# juser is a json object containing the tweets of the user
		userID = juser['user']
		tweets = []
		for jtweet in juser['tweets']:				# get the tweets objects
			tweetID = jtweet['id_str']
			tweet_time_str = "%a %b %d %H:%M:%S +0000 %Y"
			tweet_time = time.strptime(jtweet['created_at'], tweet_time_str)
			epoch = int(time.mktime(tweet_time))
			for jhashes in jtweet['entities']['hashtags']:	# get the hashtag objects
				tag = jhashes['text'].lower()		# get the hashtag text (the hashtag)
				# this will be written in the .hashtag file:
				self.add_hashtag_user( tag, userID, tweetID )	
			if len( jtweet['entities']['hashtags'] ) > 0:
				# append (so print) only the tweets tha have some hashtag
				tweets.append( (tweetID, epoch, jtweet['text']) )
		return userID, tweets					# this will be written in the .text file

	def correct_text(self, text):
		"""Cleans the text"""
		text = " ".join(text.splitlines()) # split text
		text = text.strip() # remove trailing spaces
		text = re.sub("http\:\S*", " ", text) # remove http://X
		text = re.sub("#\w*", ' ', text) # remove hashtags
		text = re.sub("@\w*", ' ', text) #remove usernames
		text = re.sub("\s+", ' ', text) # remove multiple whitespaces
		return text

	def parse(self):
		"""Since the data is so big we have to do this on the fly"""
		if self.filename[-3:] == ".xz":
			self.data = lzma.LZMAFile(self.filename)
		elif self.filename[-3:] == ".gz":
			self.data = gzip.open(self.filename)
		else:	self.data = open(self.filename)
		
		
		self.listFile = codecs.open(self.list_filename, 'w')
		self.tweetFile = codecs.open(self.text_filename, 'w', 'utf-8')
		self.hashFile = codecs.open(self.hash_filename, 'w', 'utf-8' )
		
		self.parse_data()

		self.data.close()
		self.listFile.close()
		self.tweetFile.close()
		self.hashFile.close()

	def parse_data(self):
		counter = 0
		
		print( "Extracting informations from tweet file..." )
		for tweets_to_write in self.data:
			userID, tweets = self.parse_user(json.loads(tweets_to_write))
			
			counter += 1
			if counter % 500 == 0:
				print( "Read {0} lines. Dictionary size is {1}.".format( counter, len(self.hashtags) ) )
		
			if len(tweets):
				# first prints the user
				self.listFile.write( str(userID) + ' ' )
				tweetIDs = map(lambda x: x[0], tweets)
				# then the tweet ids
				self.listFile.write( " ".join( map(str, tweetIDs) ) + '\n' )
			
			# then the tweet text
			for tweetID, time, text in tweets:
				if tweetID not in self.tweet_set :
					self.tweet_set.add( tweetID )
					self.tweetFile.write( u"{0} {1} {2}\n".format( tweetID, time, self.correct_text(text) ) )
		
		
		
		print( "Done.\nNow sorting and saving hashtags..." )
		sortedHashtags = sorted( self.hashtags.keys() ) #, key=str.lower )
		for h in sortedHashtags:
			sortedUsers = sorted( self.hashtags[h].keys() ) #ordina lessicograficamente
			tweets = ''
			for u in sortedUsers:
				tweets += " @" + str(u)
				if self.hashtags[h][u]:
					for ids in self.hashtags[h][u]:
						tweets += ' ' + str(ids)
				
			self.hashFile.write( u"{0}{1}\n".format( h, tweets ) )
		print( "Done." )
    
          


if __name__ == '__main__':
    filename = sys.argv[1]
    parser = TweetParser(filename)
    parser.parse()

