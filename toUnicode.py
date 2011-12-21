#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import re
import sys
import codecs


def replace( reMatchObject ):
	out = ''
	try:
		if ( reMatchObject.group(0)[2] == 'x' ):
			#provo con la base 16
			out = unichr( int( reMatchObject.group(0)[3:-1], 16 ) )
		else:
			#provo a convertire con la base 10
			out = unichr( int( reMatchObject.group(0)[2:-1], 10 ) )
	except ValueError:
		#altrimenti non sostituisco niente
		out = reMatchObject.group(0)
		#print( u"{0} -> {1}".format( reMatchObject.group(0), out ) )
	
	return out

def toUnicode( line ):
	return re.sub( "&#\w+;", replace, line )


if __name__ == '__main__':
	filename = sys.argv[1]
	output = codecs.open(filename + '.unicode', 'w', 'utf-8' )
	
	for line in codecs.open( filename, 'r', 'utf-8' ):
		output.write( toUnicode( line ) )
		
	output.close()
