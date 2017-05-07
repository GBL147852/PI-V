#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import stuff as s
import csv

class P(object):
	def __init__(self):
		print "parte 1!"
		self.som = s.Som(3,0,255)
		self.entradas = [
			[255,0	,0	],
			[255,255,0	],
			[0	,255,0	],
			[0	,255,255],
			[0	,0	,255],
			[255,0	,255],
		]
		self.n = 0
	
	def iteracao(self):
		self.som.atualizarPesos(self.entradas[self.n])
		self.n = (self.n+1)%len(self.entradas)
		
	def resultados(self):
		print "coisos encontrados pras entradas:\n"
		for i in self.entradas:
			valor = self.som.obterNeuronioVencedor(i)
			print "entradas:", "%.5f " * len(i) % tuple(i)
			print "neurônio vencedor:", valor[0], "x", valor[1], "\n"
			
	def matriz(self):
		return self.som.pesos