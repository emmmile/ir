#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getScore( line ):
	if line[0] == '#':
		return float( line[1:].split(' ', 1 )[0] )
	else:	return float( line.split(' ', 1 )[0] )
	
def isPolitical( line ):
	return line[0] != '#'


lines = open("precision-recall.txt").readlines()
minScore = getScore( lines[0] )
maxScore = getScore( lines[-1] )
steps = [minScore + x * 0.01 * (maxScore - minScore) for x in range(0, 100)]



print( "threshold\tprecision\trecall" )
for threshold in steps:
	posPos = 0.0		# contiene il numero di linee che parlano di politica all'interno del set +
	totalPos = 0.0		# contiene il numero totale di linee che parlano di politica 
	posSize = 0.0		# numero di elementi classificati positivi
	negSize = 0.0
	for line in lines:
		#print( line )
		if getScore( line ) < threshold:
			negSize += 1.0
		else:
			posSize += 1.0
			if isPolitical( line ):
				posPos += 1.0
		
		if isPolitical( line ):
			totalPos += 1.0
		
	print( "{0:g}\t{1:g}\t{2:g}".format( threshold, posPos / posSize, posPos / totalPos ) )
