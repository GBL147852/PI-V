#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import stuff as s

#só testes
def testes():
	som = s.Som(4,0,1)
	entradas = [
		[0.194444444,0.625,0.101694915,0.208333333],
		[0.222222222,0.541666667,0.117644068,0.166666667],
		[0.805555556,0.666666667,0.86440678,1],
		[0.555555556,0.541666667,0.847457627,1],
	]
	print "vai filho itera aí"
	n = 0
	for i in xrange(som.iteracoes):
		som.atualizarPesos(entradas[n])
		n = (n+1)%len(entradas)
	print "foi!!"
	print "coisos encontrados pras entradas:\n"
	for i in entradas:
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio:", valor[0], "x", valor[1], "\n"

#parte 1 do projeto
def parte1():
	print "parte 1!"
	som = s.Som(3,0,255)
	entradas = [
		[255,0	,0	],
		[255,255,0	],
		[0	,255,0	],
		[0	,255,255],
		[0	,0	,255],
		[255,0	,255],
	]
	print "iterando!!"
	n = 0
	for i in xrange(som.iteracoes):
		som.atualizarPesos(entradas[n])
		n = (n+1)%len(entradas)
	print "foi!!"
	print "coisos encontrados pras entradas:\n"
	for i in entradas:
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio:", valor[0], "x", valor[1], "\n"
	#falta plotar isso!

#parte 2 do projeto
def parte2():
	print "parte 2!"

#Função principal
def main():
#	testes()
	parte1()
#	parte2()
	raw_input()
main()