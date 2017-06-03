#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import MyLittlePony as mlp

width = 15
height = 15

lineIndex = 0
charIndex = 0


#transforma uma imagem em parâmetros de entrada da rede neural.
def getMlpInput(char):
	char = cv2.resize(char,(width,height),interpolation=cv2.INTER_AREA)
	mlpInput = []
	for row in img:
		for p in row:
			if p <= 0: v = 0
			elif p >= 255: v = 1
			else: v = float(p)/255
			mlpInput.append(v)
	return mlpInput
	

#reconhece um caractere de dada imagem.
def recogniseChar(img):
	#temp: salva pra gente ver isso aí
	global charIndex
	cv2.imwrite("out/char%d-%d.png" % (lineIndex,charIndex),img)
	charIndex += 1
	
	#coloca a imagem no mlp
	mlpInput = getMlpInput(img)
	#falta colocar de fato pff
	
	#temp: valor padrão
	return "A"