#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import char


#cria um fragmento de imagem binária a partir de outra e delimitada pelos dados contornos.
def createImg(img,contourList,xMin,xMax,yMin,yMax):
	
	#cria uma máscara de regiões delimitadas pelos contornos
	mask = np.zeros((yMax-yMin,xMax-xMin),np.uint8)
	mask[:] = 255
	cv2.fillPoly(mask,contourList,0,offset=(-xMin,-yMin))
	
	#retorna a máscara aplicada ao recorte da imagem
	return cv2.bitwise_or(img[yMin:yMax,xMin:xMax],mask)


#extrai contornos de uma imagem binária.
def getContours(img):
	
	#usa contornos pra procurar por caracteres
	img,contours,hierarchy = cv2.findContours(cv2.bitwise_not(img),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	#filtra e ordena os contornos encontrados
	con = []
	for (n,i) in enumerate(contours):
		
		#se ele não é um contorno externo, ignora
		if hierarchy[0][n][3] >= 0: continue
		
		#obtém a região dele
		xMin,yMin,w,h = cv2.boundingRect(i)
		xMax = xMin+w
		yMax = yMin+h
		
		#obtém o centroide
		m = cv2.moments(i)
		d = float(m["m00"])
		if d == 0: continue
		d = 1/d
		x = int(m["m10"]*d)
		y = int(m["m01"]*d)
		
		#adiciona à lista
		con.append((i,xMin,xMax,yMin,yMax,x,y))
	
	#retorna a lista de contornos
	return con


#extrai uma linha de texto de dada imagem binária. use extractText(img) em vez desse!
def extractLine(img):
	
	#loop de extração de caracteres a partir dos contornos
	chars = []
	for (contour,xMin,xMax,yMin,yMax,x,y) in getContours(img):
		
		#verifica se algum caractere tá na mesma posição x. pior caso é O(n!)...
		contourList = [contour]
		xList = [x]
		found = []
		for (m,(contourListL,xMinL,xMaxL,yMinL,yMaxL,xListL)) in enumerate(chars):
			
			#vê se o centroide dos caracteres tá dentro do intervalo dos outros
			if x < xMinL or x > xMaxL:
				for xL in xListL:
					if xL >= xMin and xL <= xMax: break
				else: continue
			
			#encontrou um caractere, põe ele na nossa lista
			found.append(m)
			contourList += contourListL
			if xMin > xMinL: xMin = xMinL
			if xMax < xMaxL: xMax = xMaxL
			if yMin > yMinL: yMin = yMinL
			if yMax < yMaxL: yMax = yMaxL
			xList += xListL
		
		#adiciona o caractere novo e remove os que foram encontrados e agrupados
		for m in reversed(found): del chars[m]
		chars.append((contourList,xMin,xMax,yMin,yMax,xList))
	
	#se nenhum caractere foi encontrado, finaliza logo
	if len(chars) == 0: return ""
	
	#ordena os caracteres no eixo x
	chars.sort(key=lambda x:x[1]+x[2])
	
	#obtém a largura esperada dos espaços a partir da média da largura dos caracteres
	spaceWidth = sum([x[2]-x[1] for x in chars])*0.3/len(chars)
	
	#e começa o reconhecimento de cada caractere!
	s = ""
	prevMax = -1
	for (n,(contourList,xMin,xMax,yMin,yMax,xList)) in enumerate(chars):
		
		#cata fragmento de imagem do caractere
		charImg = createImg(img,contourList,xMin,xMax,yMin,yMax)
		
		#tenta reconhecer o caractere. se não rolar, coloca um caractere padrão
		rec = char.recogniseChar(charImg)
		if not rec: rec = "_"
		
		#concatena com os outros caracteres já reconhecidos, considerando os espaços
		if n > 0 and xMin-prevMax >= spaceWidth:
			s += " "
		s += rec
		prevMax = xMax
	
	#retorna o resultado obtido
	return s


#extrai um bloco de texto de dada imagem.
def extractText(img):
	
	#se a imagem for vazia, ignora
	if img is None or len(img) == 0 or len(img[0]) == 0: return ""
	
	#aplica thresholding pra deixar a imagem binária
	ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	#aplica blur horizontal a fim de procurar por linhas
	img2 = cv2.blur(img,(50,5))
	ret,img2 = cv2.threshold(img2,240,255,cv2.THRESH_BINARY)
	
	#loop de extração de linhas a partir dos contornos
	lines = []
	for (contour,xMin,xMax,yMin,yMax,x,y) in getContours(img2):
		
		#verifica se alguma linha tá na mesma posição y. pior caso é O(n!)...
		contourList = [contour]
		yList = [y]
		found = []
		for (m,(contourListL,xMinL,xMaxL,yMinL,yMaxL,yListL)) in enumerate(lines):
			
			#vê se o centroide das linhas tá dentro do intervalo das outras
			if y < yMinL or y > yMaxL:
				for yL in yListL:
					if yL >= yMin and yL <= yMax: break
				else: continue
			
			#encontrou uma linha, põe ela na nossa lista
			found.append(m)
			contourList += contourListL
			if xMin > xMinL: xMin = xMinL
			if xMax < xMaxL: xMax = xMaxL
			if yMin > yMinL: yMin = yMinL
			if yMax < yMaxL: yMax = yMaxL
			yList += yListL
		
		#adiciona a linha nova e remove as que foram encontradas e agrupadas
		for m in reversed(found): del lines[m]
		lines.append((contourList,xMin,xMax,yMin,yMax,yList))
	
	#se nenhuma linha foi encontrada, finaliza logo
	if len(lines) == 0: return ""
	
	#ordena as linhas no eixo y
	lines.sort(key=lambda x:x[3]+x[4])
	
	#inicia-se a leitura de texto por linha
	s = ""
	for (n,(contourList,xMin,xMax,yMin,yMax,yList)) in enumerate(lines):
		
		#cata fragmento de imagem da linha
		lineImg = createImg(img,contourList,xMin,xMax,yMin,yMax)
		cv2.imwrite("out/line%d.png" % n,lineImg)
		
		#passa o reconhecimento da linha pra outra função
		rec = extractLine(lineImg)
		
		#concatena com as outras linhas já reconhecidas, pulando linha
		if n > 0: s += "\n"
		s += rec
	
	#retorna o bloco de texto
	return s