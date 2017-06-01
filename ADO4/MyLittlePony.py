#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random

class Neuron():
	gradient = 0
	value = 0


class NeuronLayer():
	def __init__(self, neurons):
		self.neurons = [Neuron()] * neurons
		self.numberOfNeurons = neurons


class Connection():
	def __init__(self, iLayer, jLayer):
		self.weights = [[random.uniform(0,1) for i in range(iLayer)] for j in range(jLayer)]
		self.i = iLayer
		self.j = jLayer

	def getWeight(self, i, j):
		return self.weights[i][j]


class NeuralNetwork():
	averageError = 0
	
	def __init__(self, inputNumber, classes, hiddenLayers, hiddenNeurons):
		self.layers = [0] * (hiddenLayers + 2)
		self.connections = [0] * (len(self.layers)-1)
		
		self.layers[0] = NeuronLayer(neurons = (inputNumber + 1))
		self.layers[0].neurons[0].value = 1

		self.layers[hiddenLayers+1] = NeuronLayer(neurons = classes)
		
		for i in range(1,hiddenLayers+1):
			self.layers[i] = NeuronLayer(neurons = (hiddenNeurons + 1))

		#Conexões, já com bias
		for i in range(0,hiddenLayers):
			self.connections[i] = Connection(iLayer = self.layers[i].numberOfNeurons, jLayer = (self.layers[(i+1)].numberOfNeurons - 1))
		self.connections[hiddenLayers] = Connection(iLayer = self.layers[hiddenLayers].numberOfNeurons, jLayer = (self.layers[(hiddenLayers+1)].numberOfNeurons))

		for connection in self.connections:
			for linhaPeso in connection.weights:
				print linhaPeso
			print '\n'
				

def main():
	neural = NeuralNetwork(inputNumber = 4, classes = 4, hiddenLayers = 2, hiddenNeurons = 3)

main()