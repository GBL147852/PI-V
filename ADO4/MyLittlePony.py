#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import csv
import os

class Neuron(object):
	def __init__(self):
		self.value = 0
		self.gradient = 0


class NeuronLayer(object):
	def __init__(self, neurons):
		self.neurons = []
		for i in range(neurons):
			self.neurons.append(Neuron())
		self.numberOfNeurons = neurons
		self.neurons[0].value = 1

	def SetNeuronValue(self, indice, value):
		self.neurons[indice].value = value


class Connection(object):
	def __init__(self, iLayer, jLayer):
		self.weights = [[random.uniform(0,1) for j in range(jLayer)] for i in range(iLayer)]
		self.i = iLayer
		self.j = jLayer

	def getWeight(self, i, j):
		return self.weights[i][j]


class NeuralNetwork(object):
	AvgError = 0
	PrevAvgError = 0
	LearningRage = 0.01
	Count = 1
	threshold = 0.01

	
	def __init__(self, inputNumber, classes, hiddenLayers, hiddenNeurons):
		self.layers = [0] * (hiddenLayers + 2)
		self.connections = [0] * (len(self.layers)-1)
		
		self.layers[0] = NeuronLayer(neurons = (inputNumber + 1))
		self.layers[0].neurons[0].value = 1

		self.layers[hiddenLayers+1] = NeuronLayer(neurons = classes)
		self.outputLayer = hiddenLayers+1
		self.classes = classes
		
		for i in range(1,hiddenLayers+1):
			self.layers[i] = NeuronLayer(neurons = (hiddenNeurons + 1))

		#Conexões, já com bias
		for i in range(0,hiddenLayers):
			self.connections[i] = Connection(iLayer = self.layers[i].numberOfNeurons, jLayer = (self.layers[(i+1)].numberOfNeurons - 1))
		self.connections[hiddenLayers] = Connection(iLayer = self.layers[hiddenLayers].numberOfNeurons, jLayer = (self.layers[(hiddenLayers+1)].numberOfNeurons))
				
	def Sigmoid(self, value):
		return 1 / (1 + (math.e**(-value)))

	def DerivativeSigmoid(self, value):
		return self.Sigmoid(value) * (1 - self.Sigmoid(value))

	def SetInput(self, inputs = []):
		for i in range(len(inputs)):
			self.layers[0].neurons[(i+1)].value = inputs[i]


	def AbsError(self, expected):
		errors = [0] * self.classes
		v = [0] * self.classes
		v[expected] = 1
		for n in range(self.classes):
			errors[n] = (v[n] - self.layers[self.outputLayer].neurons[n].value)
		return errors

	def QuadError(self, expected):
		error = 0
		v = [0] * self.classes
		v[expected] = 1
		AbsError = self.AbsError(expected = expected)
		for i in range(len(v)):
			error += AbsError[i]**2.0
		error /= 2.0
		return error

	def PrintRede(self):
		for layer in self.layers:
			for neuron in layer.neurons:
				print neuron.value
			print "\n"
		print '\n'


	def ForwardStep(self):
		for l in range(len(self.layers)-2):
			iLayer = self.layers[l]
			jLayer = self.layers[(l+1)]
			connection = self.connections[l]
			for j in range(connection.j):
				v = 0
				#print "Atualizando peso do neuronio ", j+1, " da camada ", l+1
				for i in range(connection.i):
					v += iLayer.neurons[i].value * connection.weights[i][j]
				
				jLayer.neurons[j+1].value = self.Sigmoid(v)

		#Última camada separada por causa do bias
		l+=1
		iLayer = self.layers[l]
		jLayer = self.layers[(l+1)]
		connection = self.connections[l]
		for j in range(connection.j):
			v = 0
			#print "Atualizando peso do neuronio ", j, " da camada ", l+1
			for i in range(connection.i):
				v += iLayer.neurons[i].value * connection.weights[i][j]
			
			jLayer.neurons[j].value = self.Sigmoid(v)

	def BackwardStep(self, errors = []):
		for l in range(len(self.layers)-1, 1, -1):
			iLayer = self.layers[(l-1)]
			jLayer = self.layers[l]

			



	def HiddenGradient(self, neuron, neuronIndex, layer, layerIndex):
		print "AAAAAAAA"
	
	def OutputGradient(self, neuron, neuronIndex):
		print "AAAAAAAA"

class Dataset(object):
	def __init__(self, path, classes):
		data = []
		dir = os.path.dirname(__file__)
		filename = os.path.join(dir, 'data/'+path+'.csv')

		with open(filename) as csvfile:
			r = csv.reader(csvfile)
			firstRow = True
			for row in r:
				if firstRow:
					firstRow = False
				else:
					data.append(list(map(float,row)))

		random.shuffle(data)
		self.data = data
		self.training = data[:(len(data)*9/10)]
		self.testing = data[(len(data)*9/10):]
		self.instances = len(data)
		self.inputs = len(data[0])-1
		self.classes = classes
		self.classIndex = 0

def main():
	dataset = Dataset(path = "iris", classes = 3)
	neural = NeuralNetwork(inputNumber = dataset.inputs, classes = 3, hiddenLayers = 2, hiddenNeurons = 3)
	while(True):
		for instance in dataset.data:
			neural.SetInput(instance[1:])
			neural.ForwardStep()
			neural.AvgError += neural.QuadError(expected = int(instance[0]))
			neural.BackwardStep(errors = neural.AbsError(expected = int(instance[0])))

		neural.AvgError /= dataset.instances
		
		print "|", neural.AvgError, " - ", neural.PrevAvgError, "| = ", abs(neural.AvgError-neural.PrevAvgError)
		if abs(neural.AvgError-neural.PrevAvgError) < neural.threshold:
			break;

		neural.PrevAvgError = neural.AvgError
		neural.AvgError = 0

main()