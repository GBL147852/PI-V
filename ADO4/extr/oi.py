#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
from matplotlib import pyplot as plt

imgOutput = None
	
def main():
	global imgOutput
	
	#escolhe arquivo
	imgPath = "line.jpg"
	
	#lê arquivo, aplica thresholding pra deixar b&w
	img = cv2.imread(imgPath,0)
	ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	imgOutput = img.copy()
	width = len(img[0])
	height = len(img)
	
	#usa contornos pra procurar por letras
	img2 = cv2.bitwise_not(img)
	img2,contours,hierarchy = cv2.findContours(img2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contourData = []
	for (n,i) in enumerate(contours):
		if hierarchy[0][n][3] >= 0: continue
		xmin,y,w,h = cv2.boundingRect(i)
		xmax = xmin+w
		m = cv2.moments(i)
		x = int(m['m10']/m['m00'])
		y = int(m['m01']/m['m00'])
		area = cv2.contourArea(i)
		contourData.append((i,xmin,xmax,x))
	
	#junta contornos em comum (mesma posição x, pra capturar acentuações, pingos no i, etc)
	letters = []
	for (n,(icontour,ixmin,ixmax,ix)) in enumerate(contourData):
		found = False
		for (m,(jcontourlist,jxmin,jxmax,jxlist)) in enumerate(letters):
			if ix >= jxmin and ix <= jxmax:
				found = True
			else:
				for jx in jxlist:
					if jx >= ixmin and jx <= ixmax:
						found = True
						break
			if found:
				contourlist = jcontourlist
				contourlist.append(icontour)
				xmin = min(jxmin,ixmin)
				xmax = max(jxmax,ixmax)
				xlist = jxlist
				xlist.append(ix)
				letters[m] = (contourlist,xmin,xmax,xlist)
				break
		if not found:
			letters.append(([icontour],ixmin,ixmax,[ix]))
	
	#desenha isso daí
	for (contourlist,xmin,xmax,xlist) in letters:
		cv2.rectangle(imgOutput,(xmin,0),(xmax,height),(128,128,128),2)
	
	#mostra na tela pls
	#plt.plot(lines)
	#plt.plot(maxs,[lines[x] for x in maxs],"ro")
	plt.imshow(imgOutput,cmap="gray",interpolation="bicubic")
	plt.xticks([]),plt.yticks([])
	plt.show()
main()