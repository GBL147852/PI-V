#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import stuff as s
import reader

#parte 1 do projeto
def parte1():
	print "parte 1!"
	
	#inicializa o filho
	som = s.Som(3,0,255)
	entradas = [
		[255,0	,0	],
		[255,255,0	],
		[0	,255,0	],
		[0	,255,255],
		[0	,0	,255],
		[255,0	,255],
	]
	
	#treina ele
	print "treinando!!", som.iteracoes, "iterações..."
	n = 0
	for i in xrange(som.iteracoes):
		som.atualizarPesos(entradas[n])
		n = (n+1)%len(entradas)
	
	#ae
	print "foi!!"
	print "coisos encontrados pras entradas:\n"
	for i in entradas:
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio vencedor:", valor[0], "x", valor[1], "\n"
	
	#falta plotar isso!

#parte 2 do projeto
def parte2():
	print "parte 2!"
	
#	dataset = "breast"
	dataset = "iris"
#	dataset = "wine"
	
	print "dataset:", dataset
	
	#carrega dataset
	dataLen,entradas,classes = reader.load(dataset)
	
	#atribui as cores abaixo às classes
	coresPossiveis = [
		[255,0,0],
		[0,255,0],
		[0,0,255],
	]
	corIndex = 0
	cores = {}
	for i in classes:
		if i not in cores:
			cores[i] = coresPossiveis[corIndex]
			corIndex += 1
	
	#inicializa e treina o guri
	som = s.Som(len(entradas[0])-1,0,1)
	print "treinando!!", som.iteracoes, "iterações..."
	n = 0
	for i in xrange(som.iteracoes):
		som.atualizarPesos(entradas[n][1:])
		n = (n+1)%len(entradas)
	
	#ae
	print "foi!!"
	print "coisos encontrados pras entradas:\n"
	for n,i in enumerate(entradas):
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio vencedor:", valor[0], "x", valor[1], "\n"
		cor = cores[classes[n]]
		#neurônio em (valor[0],valor[1]) recebe a cor acima!
		#(quando estiver plotando etc)
	

#Função principal
def main():
#	parte1()
	parte2()
	raw_input()
main()