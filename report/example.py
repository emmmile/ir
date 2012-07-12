#!/usr/bin/env python

import random
import sys
import math

def build(size):
	x = []
	for i in range(int(size)):
		x = x + [int( random.expovariate(0.9) + 1.0 )]
	return x


y = build( sys.argv[1] )
print ( ', '.join(map(str, y)) )

w = list( map( lambda x : math.log( 1.0 + x, 2 ), y ) )
out = [ len( y ), sum( w ), sum( y ) ]
print ( ', '.join(map(str, out)) )

y[2] = 15
print ( ', '.join(map(str, y)) )
w = list( map( lambda x : math.log( 1.0 + x, 2 ), y ) )
out = [ len( y ), sum( w ), sum( y ) ]
print ( ', '.join(map(str, out)) )