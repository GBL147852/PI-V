#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import stuff

#Função principal
def main():
	som = stuff.Som(4)
	entradas = [
		[0.194444444,0.625,0.101694915,0.208333333],
		[0.222222222,0.541666667,0.117644068,0.166666667],
		[0.805555556,0.666666667,0.86440678,1],
		[0.555555556,0.541666667,0.847457627,1],
	]
	print "coisos encontrados pras entradas:\n"
	for i in entradas:
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio:", valor[0], "x", valor[1], "\n"
	raw_input()
main()