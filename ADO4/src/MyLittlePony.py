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
		self.neurons[0].value = 0


class Connection(object):
	def __init__(self, iLayer, jLayer):
		self.weights = [[random.uniform(-1,1) for j in range(jLayer)] for i in range(iLayer)]
		self.i = iLayer
		self.j = jLayer


class NeuralNetwork(object):
	avgError = 0
	prevAvgError = 0
	count = 0
	
	def __init__(self, inputNumber, classes, hiddenLayers, hiddenNeurons, learningRate = 0.1, threshold = 0.05):
		self.learningRate = learningRate
		self.threshold = threshold
		
		self.layers = [0] * (hiddenLayers + 2)
		self.connections = [0] * (len(self.layers)-1)
		
		self.layers[0] = NeuronLayer(neurons = (inputNumber + 1))

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
		#print self.checkResults()
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

	def PrintNetwork(self):
		for layer in self.layers:
			for neuron in layer.neurons:
				print round(neuron.value,4), '\t',
			print ''
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
		iLayer = self.layers[len(self.layers)-2]
		jLayer = self.layers[len(self.layers)-1]
		connection = self.connections[len(self.layers)-2]
		for i in range(connection.i):
			for j in range(connection.j):
				jLayer.neurons[j].gradient = self.OutputGradient(error = errors[j], neuronValue = jLayer.neurons[j].value)
				connection.weights[i][j] += (self.learningRate * jLayer.neurons[j].gradient * iLayer.neurons[i].value)


		#print connection.weights[2][2]

		for l in range(len(self.layers)-2, 1, -1):
			iLayer = self.layers[(l-1)]
			jLayer = self.layers[l]
			connection = self.connections[(l-1)]
			for i in range(connection.i):
				for j in range(connection.j):
					jLayer.neurons[j+1].gradient = self.HiddenGradient(neuronValue = jLayer.neurons[j+1].value, neuronIndex = j, layerIndex = l-1)
					connection.weights[i][j] += (self.learningRate * jLayer.neurons[j+1].gradient * iLayer.neurons[i].value)

	def checkResults(self):
		greaterResult = 0
		greaterIndex = -1

		for i in range(len(self.layers[self.outputLayer].neurons)):
			# print "Checagem: ", i, " - ", self.layers[self.outputLayer].neurons[i].value
			if self.layers[self.outputLayer].neurons[i].value >= greaterResult:
				greaterIndex = i
				greaterResult = self.layers[self.outputLayer].neurons[i].value
		return (greaterIndex,greaterResult)

	# def TestingSet(self, inputs = [[]]):
	# 	countRight = 0
	# 	for entrance in inputs:
	# 		attributes = entrance[1:]
	# 		expected = int(entrance[0])
	# 		self.SetInput(attributes)
	# 		self.ForwardStep()
	# 		# self.PrintNetwork()
	# 		print self.checkResults(), " - ", expected
	# 		if(self.checkResults()[0] == expected):
	# 			countRight += 1
	# 		# raw_input()
	# 	print countRight, " out of ", len(inputs)
	# 	return float(countRight)/float(len(inputs)) * 100


	def HiddenGradient(self, neuronValue, neuronIndex, layerIndex):
		kLayer = self.layers[layerIndex+1]
		connection = self.connections[layerIndex].weights
		sequence = 0
		for k in range(1,len(kLayer.neurons)):
			sequence += connection[neuronIndex+1][k-1] * kLayer.neurons[k-1].gradient
		return sequence * self.DerivativeSigmoid(value = neuronValue)
	
	def OutputGradient(self, error, neuronValue):
		return (error * self.DerivativeSigmoid(value = neuronValue))

	def loadTraining(self, trainingPath):
		with open(trainingPath) as csvfile:
			r = csv.reader(csvfile)
			connection = -1
			i = 0
			for row in r:
				if len(row) < 3:
					
					connection +=1
					i = 0
					print 'Conexao da camada ', connection , ' para a camada ', connection+1, ' carregada!'
				else:
					self.connections[connection].weights[i] = list(map(float,row))
					i += 1

	def saveTraining(self, trainingPath):
		with open(trainingPath,"wb") as csvfile:
			writer = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL)
			for connection in self.connections:
				writer.writerow([connection.i,connection.j])
				writer.writerows(connection.weights)
		print 'CSV de treinamento construido!'

class Dataset(object):
	def __init__(self, inputs = 0, classes = 0):
		self.data = []
		self.training = []
		self.testing = []
		self.inputs = inputs
		self.classes = classes
	
	def loadCsv(self, name, inputs = 0, classes = 0):
		data = []
		dir = os.path.dirname(__file__)
		filename = os.path.join(dir, '../data/'+name+'/data.csv')

		with open(filename) as csvfile:
			r = csv.reader(csvfile)
			firstRow = True
			for row in r:
				if firstRow:
					firstRow = False
				else:
					data.append(list(map(float,row)))

		self.data = data
		self.inputs = inputs if inputs > 0 else len(data[0])-1
		self.classes = classes if classes > 0 else self.classes
		self.name = name
		self.path = 'data/'+name+'/'
	
	def setTrainingAndTesting(self):
		random.shuffle(self.data)
		trainLen = len(self.data)*1
		self.training = self.data[:trainLen]
		self.testing = self.data[trainLen:]