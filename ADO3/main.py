#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import som as s
import reader
import window

def parte1(iteracoesPorFrame=1,largura=0):
	print "parte 1!"
	
	#inicializa tudo
	atributos = 3
	if largura <= 0:
		largura = s.quadradoMaisProximo(atributos)
	som = s.Som(atributos=atributos,largura=largura,pesoMin=0,pesoMax=255)
	entradas = [
		[255,0	,0	],
		[255,255,0	],
		[0	,255,0	],
		[0	,255,255],
		[0	,0	,255],
		[255,0	,255],
	]
	n = 0
	
	#loop da janela
	while True:
		printEnd = 0
		if window.loop():
			if som.n < som.iteracoes:
				print "iteração", som.n, "/", som.iteracoes
				for i in xrange(min(iteracoesPorFrame,som.iteracoes-som.n)):
					som.atualizarPesos(entradas[n])
					n = (n+1)%len(entradas)
				if som.n >= som.iteracoes:
					print "fim das iterações!"
					printEnd = 1
			window.drawMatrix(som.pesos)
			window.frameEnd()
		else:
			printEnd = 2
		if printEnd > 0:
			print "coisos encontrados pras entradas:\n"
			for i in entradas:
				valor = som.obterNeuronioVencedor(i)
				print "entradas:", "%.5f " * len(i) % tuple(i)
				print "neurônio vencedor:", valor[0], "x", valor[1], "\n"
			if printEnd == 2: break

def parte2(dataset,largura=0):
	print "parte 2!"
	
	#carrega o dataset e inicializa tudo
	dataLen,entradas,classes = reader.load(dataset)
	atributos = len(entradas[0])-1
	if largura <= 0:
		largura = s.quadradoMaisProximo(len(entradas[0])-1)
	som = s.Som(atributos=atributos,largura=largura,pesoMin=0,pesoMax=1)
	n = 0
	
	#atribui as cores abaixo às classes
	coresPossiveis = [
		[255,0,0],
		[0,255,0],
		[0,0,255],
	]
	cores = {}
	for i in classes:
		if i not in cores:
			cores[i] = coresPossiveis[0]
			coresPossiveis = coresPossiveis[1:]
	
	#itera!
	print "iterando...", som.iteracoes
	while som.n < som.iteracoes:
		som.atualizarPesos(entradas[n][1:])
		n = (n+1)%len(entradas)
	
	#resultados + cria a matriz final
	matriz = [[[0 for x in xrange(3)] for i in xrange(som.largura)] for j in xrange(som.largura)]
	print "coisos encontrados pras entradas:\n"
	for n,i in enumerate(entradas):
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio vencedor:", valor[0], "x", valor[1], "\n"
		matriz[valor[0]][valor[1]] = cores[classes[n]]
	
	#loop da janela
	while window.loop():
		window.drawMatrix(matriz)
		window.frameEnd()
			
def main():
	window.start()
	parte1(largura=25,iteracoesPorFrame=50)
#	parte2(dataset="breast")
#	parte2(dataset="iris")
#	parte2(dataset="wine")
	window.end()
main()