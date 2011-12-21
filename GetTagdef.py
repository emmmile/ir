#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import urllib2
import json
import codecs
import sys
import os

class GetTagdef(object):

	def __init__(self, filename):
		self.filename = filename
		#name, ext = os.path.splitext(self.filename)
		self.def_filename = self.filename + ".tagdef"
		self.err = codecs.open("errorDescriptionTag.txt", 'w')

	def tagRequest(self, tag):		#recupera le definizioni di un dato hashtag "tag"
		tagDef = []
		host = "http://api.tagdef.com/"+tag+".json"
		try:
			response_stream = urllib2.urlopen(host)
		except urllib2.HTTPError, e:
			self.err.write("HTTP Error "+str(e.code))
		except urllib2.URLError, e:
			self.err.write("URLError "+str(e.code))
		else:
			jsonTag = json.loads(response_stream.read())	#legge le def sottoforma di JSON dal server api.tagdef
			response_stream.close()

			for d in jsonTag['defs']:	# get the defs objects
				tagDef.append(d['def']['text']) #aggiunge una def
			return tagDef

	def getTags(self, filename):
		tags = []
		for line in filename:
			token = line.split(' ',1)
			tags.append(token[0])
		return tags

	def searchDef(self):
		filename = open(self.filename)
		def_filename = codecs.open(self.def_filename, 'w', 'utf-8')
		tags = self.getTags(filename) #lista dei tags letta da file
		for t in tags:
			if self.tagRequest(t):
				definitions = list(enumerate(self.tagRequest(t))) #lista di tuple (count "i" , value in pos "i")
				def_filename.write(u" {0} {1}\n".format(t, ' '.join( map(lambda x: str(x[0]) + ") "+ x[1], definitions) )))
		filename.close()
		def_filename.close()
		self.err.close()

if __name__ == '__main__':
    filename = sys.argv[1]
    tags = GetTagdef(filename)
    tags.searchDef()

