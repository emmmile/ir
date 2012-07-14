#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
import toUnicode

class lineNoMatch(object):

	def __init__(self, filetext):
		self.fileT = filetext

	def printLine(self):
		self.dataT = open(self.fileT)
		counter = 0;
		for line in self.dataT:
			counter += 1
			if counter % 10000 == 0:
				print( "Read {0} lines.".format( counter) )
			if(re.match("[\d]+\t[\d]+\t*",line) == None):
				print(line)

		self.dataT.close()

if __name__ == '__main__':
	filetext = sys.argv[1]
	noMatch = lineNoMatch(filetext)
	noMatch.printLine()
