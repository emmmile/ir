#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Crea un grafo casuale. Da usare poi con graph.py
"""

import sys
import random

class Graph ( object ):
	def build ( self, fileName ):
		output = open( fileName, 'w' )
		random.seed()
		politicians = set()
		
		for i in range( 0, 100 ):
			pol = random.randint( 1, 100000000 )
			politicians.add( pol )
			output.write( str( pol ) + '\n' )
			while random.randint( 0, 20000 ) != 11:
				
				user = random.randint( 1, 100000000 )
				while user in politicians:
					user = random.randint( 1, 100000000 )
				
				output.writelines( str( user ) + '\n' )
			output.write( '\n' )
		output.close()
			
		
if __name__ == '__main__':
	assert( len(sys.argv) == 2 )
	graph = Graph()
	print( 'Creating the random graph file...' )
	graph.build( sys.argv[1] )
	print( 'Created.' )

