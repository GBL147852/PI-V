#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import som as s
import reader
import window

#parte 1 dos resultados (cores)
def parte1(iteracoesPorFrame=1,largura=0,iteracoes=0,cores=0,aprendizado=0):
	print "parte 1!\n"
	
	#entradas fixas. vermelho, amarelo, verde, turquesa, azul, rosa
	entradas = [
		[255,0,0],
		[255,255,0],
		[0,255,0],
		[0,255,255],
		[0,0,255],
		[255,0,255],
	]
	if cores > 0:
		entradas = entradas[:cores]
	else:
		cores = len(entradas)
	atributos = 3
	n = 0
	
	#inicializa o som
	if largura <= 0: largura = s.quadradoMaisProximo(cores)
	som = s.Som(atributos=atributos,largura=largura,pesoMin=0,pesoMax=255)
	if iteracoes > 0: som.iteracoes = iteracoes
	if aprendizado > 0: som.N0 = aprendizado
	
	#loop da janela
	while True:
		printEnd = 0
		if window.loop():
			
			#realiza as iterações restantes
			if som.n < som.iteracoes:
				print "iteração", som.n, "/", som.iteracoes
				for i in xrange(min(iteracoesPorFrame,som.iteracoes-som.n)):
					
					#aqui acontece a atualização dos pesos de fato
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
			
			#printa os resultados no fim das iterações
			print "\nentradas e neurônios vencedores correspondentes:"
			for i in entradas:
				neu = som.obterNeuronioVencedor(i)
				print i, "->", neu
			if printEnd == 2: break

#parte 2 dos resultados (dataset)
def parte2(dataset,largura=0):
	print "parte 2!\n"
	
	#carrega o dataset.
	#o primeiro valor de cada linha do dataset é a classe,
	#então ignoramos essa coluna sempre que possível
	data = reader.load(dataset)
	atributos = len(data[0])-1
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
	
	#inicializa o som
	if largura <= 0: largura = s.quadradoMaisProximo(len(cores))
	som = s.Som(atributos=atributos,largura=largura,pesoMin=0,pesoMax=1)
	
	#itera!
	print "número de iterações:", som.iteracoes
	print "iterando..."
	while som.n < som.iteracoes:
		
		#atualização dos pesos aqui
		som.atualizarPesos(data[n][1:])
		n = (n+1)%len(data)
		
	print "fim das iterações!\n"
	
	#cria a matriz de cores que será apresentada no loop da janela
	matriz = [[[0 for x in xrange(3)] for i in xrange(som.largura)] for j in xrange(som.largura)]
	for i in data:
		neu = som.obterNeuronioVencedor(i[1:])
		matriz[neu[0]][neu[1]] = cores[i[0]]
		
	#printa infos sobre as classes e as cores
	print "classes e cores correspondentes:"
	for k,v in cores.iteritems():
		print "%d" % k, "->", v
	
	#loop da janela
	while window.loop():
		window.drawMatrix(matriz)
		window.frameEnd()
		
#método principal
def main():
	print "\n"
	window.start()
	
#	parte1(iteracoesPorFrame=50)
#	parte2(dataset="breast")
	parte2(dataset="iris")
#	parte2(dataset="wine")
	
	window.end()
	print "\n"
main()