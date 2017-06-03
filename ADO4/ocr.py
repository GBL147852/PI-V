#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import src.extr as extr


#loop principal
print("\n[envie uma linha vazia para finalizar.]\n")
while True:
	
	#obtém o input do usuário, finaliza se for uma linha vazia
	s = raw_input("~ caminho da imagem: ")
	if not s: break
	
	#abre o arquivo selecionado
	img = cv2.imread(s,0)
	if img is None or len(img) == 0 or len(img[0]) == 0:
		print("~ imagem inválida!")
		continue
	
	#extrai o texto da imagem
	txt = extr.extractText(img)
	
	#imprime na tela o texto extraído
	print("~ texto extraído:\n\n%s\n" % txt)

#fim!
print("\n")