#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import os

def load(path):
	entrada = []
	classe = []
	length = 0
	dir = os.path.dirname(__file__)
	filename = os.path.join(dir, 'data/'+path+'.csv')
	
	with open(filename) as csvfile:
		r = csv.reader(csvfile)
		firstRow = True
		for row in r:
			if firstRow:
				firstRow = False
			else:
				entrada.append(list(map(float,row[1:])))
				classe.append(row[0])
				length += 1
	return length,entrada,classe