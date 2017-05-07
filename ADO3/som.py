#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random


#Retorna o quadrado perfeito mais próximo de um valor n
def quadradoMaisProximo(n):
	return int(math.ceil(math.sqrt(n*10)))
	
	
#Retorna a distância euclidiana quadrática entre x e y, dado d dimensões
def distanciaQuadratica(x,y,d):
	dist = 0
	for i in range(d):
		dist += (x[i]-y[i])**2
	return dist
	
	
#Retorna a distância euclidiana entre x e y, dado d dimensões
def distancia(x,y,d):
	return math.sqrt(distanciaQuadratica(x,y,d))
	
	
class Som(object):
	#número de iterações
	n = 0
	
	#Desvio Padrão, ou σ(0)
	SIGMA0 = 2
	#T1 dado no enunciado
	T1 = 3321.92
	#η(0), ou seja, taxa de aprendizado
	N0 = 0.1
	#T(2) dado no enunciado
	T2 = 1000
	#Raio de vizinhança do neurônio vencedor
	R = 3
	
	
	#η(n), ou seja, taxa de aprendizado no momento n
	def eta(self):
		return self.N0 * (math.pow( math.e , -self.n/self.T2 ))
		
		
	#σ(n), ou seja, desvio padrão no momento n
	def sigma(self):
		return self.SIGMA0 * (math.pow( math.e , self.n/self.T1 ))
		
		
	#inicializa o objeto com o tanto de atributos das entradas
	def __init__(self,atributos,largura,pesoMin,pesoMax):
		self.atributos = atributos
		self.largura = largura
		self.iteracoes = (self.largura**2)*500
		#Pego o quadrado mais próximo (i) da quantidade de atributos (a) e assim assumo uma matriz x[i][i][a]
		self.pesos = [[[random.uniform(pesoMin,pesoMax) for x in xrange(self.atributos)] for i in xrange(self.largura)] for j in xrange(self.largura)]
		
		
	#calcula o neurônio vencedor para as entradas dadas
	def obterNeuronioVencedor(self,entradas):
		menorI = -1
		menorJ = -1
		menorDist = -1
		for i in range(self.largura):
			for j in range(self.largura):
				dist = distanciaQuadratica(entradas,self.pesos[i][j],self.atributos)
				#se essa for a menor distância calculada (ou a primeira entrada),
				#assume este neurônio como vencedor
				#(fun fact, não precisa calcular a raiz da distância)
				if menorDist < 0 or menorDist > dist:
					menorI = i
					menorJ = j
					menorDist = dist
		return (menorI,menorJ)
		
		
	#atualiza os valores dos neurônios de acordo com uma nova entrada
	def atualizarPesos(self,entradas):
		
		#obtém o neurônio vencedor
		nv = self.obterNeuronioVencedor(entradas)
		
		#pré-calculando coisas! viva performance
		raioQuadrado = self.R**2
		eta = self.eta()
		expParcial = -1/(2*(self.sigma()**2))
		
		#calcula os intervalos de atualização de acordo com o raio
		irange = range(max(nv[0]-self.R,0),min(nv[0]+self.R+1,self.largura))
		jrange = range(max(nv[1]-self.R,0),min(nv[1]+self.R+1,self.largura))
		
		#atualiza o peso da galera
		for i in irange:
			for j in jrange:
				dist = (i-nv[0])**2 + (j-nv[1])**2
				if dist > raioQuadrado: continue
				etah = eta*math.pow(math.e,dist*expParcial)
				for x in xrange(self.atributos):
					self.pesos[i][j][x] += etah*(entradas[x]-self.pesos[i][j][x])
					
		#:3c
		self.n += 1
		
		