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


#Inicia randomicamente a matriz de pesos para cada atributo no mapa
def iniciarPesos(atributos):
	i = quadradoMaisProximo(atributos)
	#Traduzindo: Pego o quadrado mais próximo (i) da quantidade de atributos (a)
	#			 e assim assumo uma matriz x[i][i][a]
	return [[[random.random() for col in range(i)]for row in range(i)] for x in range(atributos)]
	
	
#Função principal	
def main():
	i = 1
	#Propositalmente, a distância de 1, para que h(0) de 0.882497,
	#assim como no gráfico do enunciado (que eu corrigi pro Ilha)
	A = [2,2]
	B = [3,2]
	atributos = 4
	#Inicia a matriz de pesos que liga cada atributo ao mapa
	x = iniciarPesos(atributos)
	for a in x:
		print "Mapa de pesos do atributo " , i , "\n"
		for linha in a:
			#Printa cada vetor, arredondando em 5 casas decimais
			print "%.5f " * len(linha) % tuple(linha)
		print "\n\n"	
		i+=1
	print "- h(0) =\t" , h(A,B,0)
	print "- Eta(0) =\t" , eta(0)
	print "- Sigma(0) =\t" , sigma(0)
	print "- Quadrado mais proximo de 4*10= " , quadradoMaisProximo(4)
	raw_input()
main()