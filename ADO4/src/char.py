#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import MyLittlePony as mlp
import csv
import math
import os

width = 12
height = 12
characters = []
nn = None


#carrega dados do conjunto de caracteres a ser utilizado.
def loadData(name):
	global width
	global height
	global characters
	global nn
	
	dir = os.path.dirname(__file__)
	classes = os.path.join(dir, "../data/"+name+"/classes.csv")
	options = os.path.join(dir, "../data/"+name+"/options.csv")
	
	characters = []
	with open(classes) as csvfile:
		r = csv.reader(csvfile)
		firstRow = True
		for row in r:
			if firstRow: firstRow = False
			else: characters.append(str(row[1]))
	
	with open(options) as csvfile:
		r = csv.reader(csvfile)
		for (n,row) in enumerate(r):
			if n == 0: width = int(row[1])
			if n == 1: height = int(row[1])
	
	#etc
	
	nn = mlp.NeuralNetwork(inputNumber=width*height,classes=len(characters),hiddenLayers=3,hiddenNeurons=int(math.sqrt(width*height*len(characters))))


#transforma uma imagem em parâmetros de entrada da rede neural.
def getMlpInput(img):
	
	#verifica o tamanho. se for 0, já retorna uma lista vazia
	yMin = 0
	yMax = len(img)
	if yMax == 0: return [0 for i in width*height]
	xMin = 0
	xMax = len(img[0])
	if xMax == 0: return [0 for i in width*height]
	
	#recorta a imagem até os pixels pretos
	while yMin < yMax:
		row = img[yMin]
		for i in row:
			if i == 0: break
		else:
			yMin += 1
			continue
		break
	else: return [0 for i in width*height]
	while yMin < yMax:
		row = img[yMax-1]
		for i in row:
			if i == 0: break
		else:
			yMax -= 1
			continue
		break
	else: return [0 for i in width*height]
	while xMin < xMax:
		for i in xrange(yMin,yMax):
			if img[i,xMin] == 0: break
		else:
			xMin += 1
			continue
		break
	else: return [0 for i in width*height]
	while xMin < xMax:
		for i in xrange(yMin,yMax):
			if img[i,xMax-1] == 0: break
		else:
			xMax -= 1
			continue
		break
	else: return [0 for i in width*height]
	
	#redimensiona a imagem pro tamanho desejado
	img = cv2.resize(img[yMin:yMax,xMin:xMax],(width,height),interpolation=cv2.INTER_AREA)
	
	#transforma em um array normalizado
	mlpInput = []
	for row in img:
		for p in row:
			if p <= 0: v = 1
			elif p >= 255: v = 0
			else: v = 1-(float(p)/255)
			mlpInput.append(v)
	
	#retorna o array normalizado
	return mlpInput
	

#reconhece um caractere de dada imagem.
def recogniseChar(img):
	#coloca a imagem no mlp
	mlpInput = getMlpInput(img)
	nn.SetInput(mlpInput)
	nn.ForwardStep()
	
	#obtém o resultado. se for válido, o retorna
	index,value = nn.checkResults()
	if index >= 0 and index < len(characters): return characters[index]
	return ""