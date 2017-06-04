#!/usr/bin/python
# -*- coding: UTF-8 -*-

import zipfile
import numpy as np
import cv2
import src.char as char
import csv
import math


#início
print("\n[pré-processador de datasets de caracteres]\n")
s = raw_input("~ digite o nome da pasta do dataset: ")
char.width = int(raw_input("~ largura desejada do caractere: "))
char.height = int(raw_input("~ altura desejada do caractere: "))
classes = []

#cria o csv de dados
with open("data/"+s+"/data.csv","wb") as csvfile:
	writer = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["Class"]+["P"+str(x) for x in xrange(char.width*char.height)])
	with zipfile.ZipFile("data/"+s+"/img.zip","r") as zfile:
		for file in zfile.infolist():
			print(file.filename)
			c = int(file.filename.split("-")[0])
			if c not in classes: classes.append(c)
			img = cv2.imdecode(np.frombuffer(zfile.read(file.filename),np.uint8),0)
			writer.writerow([str(c)]+[str(x) for x in char.getMlpInput(img)])

#cria o csv de opções dos dados
with open("data/"+s+"/options.csv","wb") as csvfile:
	writer = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["Character width",str(char.width)])
	writer.writerow(["Character height",str(char.height)])
	writer.writerow(["Classes",str(len(classes))])

print("~ dataset gerado!")