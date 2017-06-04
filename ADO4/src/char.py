#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
#import MyLittlePony as mlp

width = 12
height = 12


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
	#falta colocar de fato pff
	
	#temp: valor padrão
	return "A"