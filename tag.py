#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-


# Prende in input una frase e propone degli hashtags con cui taggarla
# Utilizza una parte in java che scrive nel file ./.tmp i topic trovati nella frase


import sys
import os
from subprocess import call

tmp = ".tmp"
text = sys.argv[1]
frequencyPrefix = "f="
usersPrefix = "u="




call( ["java", "-Xmx2G", "AnnotateText", tmp, "\"" + text + "\""], stdout = open(os.devnull, 'wb') )

lines = []
for line in open( "data/allusers/allusers.topics" ):
	lines.append( line )

results = dict()

for t in open( tmp ):
	topic = t.rstrip()
	print( topic )
	for line in lines:
		if line.find( topic ) == -1:
			continue
		
		tags = line.rstrip().split( ' #' )
		for t in tags[1:]:
			#print( t )
			h,f,u = t.split()
			freq = int(f.replace(frequencyPrefix, ""))
			users = int(u.replace(usersPrefix, ""))
			if h not in results:
				results[h] = [freq, users]
			else:
				results[h][0] += freq
				results[h][1] += users

print( "You may consider to tag '" + text + "' with these hashtags:\n" )

sortedTags = sorted( results, key=lambda x: -results[x][1] )
for h in sortedTags[:10]:
	print( "  #" + h + " " + frequencyPrefix + str( results[h][0] ) + " " + usersPrefix + str( results[h][1] ) )
	
	
call( ["rm", tmp ] )

