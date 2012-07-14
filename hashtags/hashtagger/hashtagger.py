#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-


# Prende in input una frase e propone degli hashtags con cui taggarla
# Utilizza una parte in java che scrive nel file ./.tmp i topic trovati nella frase


import sys
import os
from subprocess import call

tmp = ".tmp"
text = sys.argv[2]
topicsfile = sys.argv[1]
#frequencyPrefix = "f="
#usersPrefix = "u="
scorePrefix = "s="



call( ["java", "-Xmx2G", "AnnotateText", tmp, "\"" + text + "\""], stdout = open(os.devnull, 'wb') )

lines = []
for line in open( topicsfile ):
#for line in open( "../../data/i3terroni-dataset/hashtags-filtered/with-hashtags.cleaned.annotation" ):
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
			h,s = t.split()
			score = float(s.replace(scorePrefix, ""))
			#h,s,u = t.split()
			#freq = int(f.replace(frequencyPrefix, ""))
			#users = int(u.replace(usersPrefix, ""))
			if h not in results:
				results[h] = score#[freq, users]
			else:
				results[h] += score#freq
				#results[h][1] += users

print( "You may consider to tag '" + text + "' with these hashtags:\n" )

sortedTags = sorted( results, key=lambda x: -results[x] )
for h in sortedTags[:10]:
	print( "  #" + h + " " + scorePrefix + str( results[h] ) ) # + " " + usersPrefix + str( results[h][1] ) )
	
	
call( ["rm", tmp ] )

