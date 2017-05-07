#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import csv
import os

def load(path):
	data = []
	dir = os.path.dirname(__file__)
	filename = os.path.join(dir, 'data/'+path+'.csv')
	
	with open(filename) as csvfile:
		r = csv.reader(csvfile)
		firstRow = True
		for row in r:
			if firstRow:
				firstRow = False
			else:
				data.append(list(map(float,row)))
				
	random.shuffle(data)
	return data