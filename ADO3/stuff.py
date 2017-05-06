#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random

#Constantes#

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


#Retorna o quadrado perfeito mais próximo de um valor n
def quadradoMaisProximo(n):
	return int(math.ceil(math.sqrt(n*10)))
	
	
#η(n), ou seja, taxa de aprendizado no momento n
def eta(n):
	return N0 * (math.pow( math.e , -n/T2 ))
	
	
#σ(n), ou seja, desvio padrão no momento n
def sigma(n):
	return SIGMA0 * (math.pow( math.e , n/T1 ))
	
	
#Retorna a distância euclidiana quadrática entre x e y, dado d dimensões
def distanciaQuadratica(x, y, d):
	dist = 0
	for i in range(d):
		dist += (x[i]-y[i])**2
	return dist
	
	
#Retorna a distância euclidiana entre x e y, dado d dimensões
def distancia(x, y, d):
	return math.sqrt(distanciaQuadratica(x,y,d))
	
	
#Retorna o h_j,i_(n) dada a distância quadrática entre os pontos
def h(d,n):
	expoente = (-d) / (2 * (sigma(n)**2) )
	return math.pow( math.e , expoente )
	
	
#classes!!!!!
class Som(object):
	#inicializa o objeto com o tanto de atributos das entradas
	def __init__(self,entradasLen):
		self.n = 0
		self.entradasLen = entradasLen
		self.largura = quadradoMaisProximo(entradasLen)
		self.iteracoes = (self.largura**2)*500
		#Traduzindo: Pego o quadrado mais próximo (i) da quantidade de atributos (a)
		#			 e assim assumo uma matriz x[i][i][a]
		self.pesos = [[[random.random() for x in range(self.entradasLen)]for i in range(self.largura)] for j in range(self.largura)]
			
		
	#calcula o neurônio vencedor para as entradas dadas
	def obterNeuronioVencedor(self,entradas):
		menorI = -1
		menorJ = -1
		menorDist = -1
		for i in range(self.largura):
			for j in range(self.largura):
				dist = distanciaQuadratica(entradas,self.pesos[i][j],self.entradasLen)
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
		nv = self.obterNeuronioVencedor(entradas)
		for x in xrange(self.entradasLen):
			peso = self.pesos[nv[0]][nv[1]][x]
			peso += eta(self.n)*(entradas[x]-peso)
			self.pesos[nv[0]][nv[1]][x] = peso
		irange = range(max(nv[0]-R,0),min(nv[0]+R+1,self.largura))
		jrange = range(max(nv[1]-R,0),min(nv[1]+R+1,self.largura))
		Rquadrado = R*R
		for i in irange:
			for j in jrange:
				dist = (i-nv[0])**2 + (j-nv[1])**2
				if dist <= Rquadrado:
					for x in xrange(self.entradasLen):
						peso = self.pesos[i][j][x]
						peso += eta(self.n)*h(dist,self.n)*(entradas[x]-peso)
						self.pesos[i][j][x] = peso
		self.n += 1