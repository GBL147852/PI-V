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
	if largura <= 0: largura = s.quadradoMaisProximo(atributos)
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
				neu = som.obterNeuronioVencedor(i)
				print "entradas:", "%.5f " * len(i) % tuple(i)
				print "neurônio vencedor:", neu[0], "x", neu[1], "\n"
			if printEnd == 2: break

def parte2(dataset,largura=0):
	print "parte 2!"
	
	#carrega o dataset e inicializa tudo
	data = reader.load(dataset)
	atributos = len(data[0])-1
	if largura <= 0: largura = s.quadradoMaisProximo(atributos)
	som = s.Som(atributos=atributos,largura=largura,pesoMin=0,pesoMax=1)
	n = 0
	
	#atribui as cores abaixo às classes
	coresPossiveis = [
		[255,0,0],
		[0,255,0],
		[0,0,255],
	]
	cores = {}
	for i in data:
		if i[0] not in cores:
			cores[i[0]] = coresPossiveis[0]
			coresPossiveis = coresPossiveis[1:]
	
	#itera!
	print "iterando...", som.iteracoes
	while som.n < som.iteracoes:
		som.atualizarPesos(data[n][1:])
		n = (n+1)%len(data)
	
	#cria a matriz final
	matriz = [[[0 for x in xrange(3)] for i in xrange(som.largura)] for j in xrange(som.largura)]
	for i in data:
		neu = som.obterNeuronioVencedor(i[1:])
		matriz[neu[0]][neu[1]] = cores[i[0]]
		
	#infos das cores
	for k,v in cores.iteritems():
		print "classe", "%d" % k, "-> cor", v
	
	#loop da janela
	while window.loop():
		window.drawMatrix(matriz)
		window.frameEnd()
			
def main():
	window.start()
#	parte1(largura=25,iteracoesPorFrame=50)
#	parte2(dataset="breast")
	parte2(dataset="iris")
#	parte2(dataset="wine")
	window.end()
main()