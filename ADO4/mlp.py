#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import csv
import os
import src.MyLittlePony as mlp



dataset = mlp.Dataset()
dataset.loadCsv(name = 'iris', classes = 3)
dataset.setTrainingAndTesting()
neural = mlp.NeuralNetwork(inputNumber = dataset.inputs, classes = dataset.classes, hiddenLayers = 2, hiddenNeurons = 9)
# maxIter = 200
print '=== DATASET INFO ===\n'
v = [0] * dataset.classes
for instance in dataset.training:
	v[int(instance[0])] +=1
print v, " - Treinamento (Classes)"
v = [0] * dataset.classes
for instance in dataset.testing:
	v[int(instance[0])] +=1
print v, " - Teste (Classes)"
print '\n'
print '=== TRAINING INFO ===\n'
while(True):
	# print round((float(neural.Count)/float(maxIter))*100.0,2), '% treinados'
	for instance in dataset.training:
		neural.SetInput(instance[1:])
		neural.ForwardStep()
		neural.avgError += neural.QuadError(expected = int(instance[0]))
		neural.BackwardStep(errors = neural.AbsError(expected = int(instance[0])))
	neural.avgError /= len(dataset.training)
	neural.count += 1

	#print "|", neural.AvgError, " - ", neural.PrevAvgError, "| = ", abs(neural.AvgError-neural.PrevAvgError)
	#if abs(neural.AvgError - neural.PrevAvgError) < neural.threshold:
	#	break;

	if neural.avgError < neural.threshold:
		break;

	neural.prevAvgError = neural.avgError
	neural.avgError = 0
print '\n'
print '=== TESTING INFO ===\n'
print neural.TestingSet(inputs = dataset.testing)

print '\n'
print '=== STATISTICS ===\n'
neural.PrintNetwork()

# print '\n Adicionando o input [0,0,0,0]\n'
# neural.SetInput([0,0,0,0])
# neural.ForwardStep()
# neural.PrintNetwork()