#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv

def load(path):
	entrada = []
	classe = []
	length = 0
	with open('data/'+path+'.csv') as csvfile:
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