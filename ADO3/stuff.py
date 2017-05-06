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
	
	
#Retorna a distância euclidiana entre x e y, dado d dimensões
def distanciaEuclidiana(x, y, d):
    distancia = 0
    for i in range(d):
		distancia += pow((x[i] - y[i]), 2)
    return math.sqrt(distancia)
    
	
#Retorna o h_j,i_(n)
def h(nx,ny,n):
	expoente = (-((distanciaEuclidiana(nx,ny,2))**2)) / (2 * (sigma(n)**2) )
	return math.pow( math.e , expoente )
	
	
#classes!!!!!
class Som(object):
	#inicializa o objeto com o número de atributos desejado
	def __init__(self,atributos):
		self.atributos = atributos
		self.largura = quadradoMaisProximo(atributos)
		#Traduzindo: Pego o quadrado mais próximo (i) da quantidade de atributos (a)
		#			 e assim assumo uma matriz x[i][i][a]
		self.pesos = [[[random.random() for x in range(self.atributos)]for i in range(self.largura)] for j in range(self.largura)]
			
		
	#calcula o neurônio vencedor para as entradas dadas
	def obterNeuronioVencedor(self,entradas):
		menorI = -1
		menorJ = -1
		menorDist = -1
		for i in range(self.largura):
			for j in range(self.largura):
				dist = 0
				for n,x in enumerate(entradas):
					dist += (x-self.pesos[i][j][n])**2
				#se essa for a menor distância calculada (ou a primeira entrada),
				#assume este neurônio como vencedor
				#(fun fact, não precisa calcular a raiz da distância)
				if menorDist < 0 or menorDist > dist:
					menorI = i
					menorJ = j
					menorDist = dist
		return (menorI,menorJ)