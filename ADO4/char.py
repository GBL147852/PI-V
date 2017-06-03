#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2

lineIndex = 0
charIndex = 0

#reconhece um caractere de dada imagem.
def recogniseChar(char):
	#temp: salva pra gente ver isso aí
	global charIndex
	cv2.imwrite("out/char%d-%d.png" % (lineIndex,charIndex),char)
	charIndex += 1
	
	#temp: valor padrão
	return "A"