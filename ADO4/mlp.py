#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import csv
import os
import src.MyLittlePony as mlp



dataset = mlp.Dataset(path = "iris", classes = 3)
neural = mlp.NeuralNetwork(inputNumber = dataset.inputs, classes = 3, hiddenLayers = 2, hiddenNeurons = 9)
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
		neural.AvgError += neural.QuadError(expected = int(instance[0]))
		neural.BackwardStep(errors = neural.AbsError(expected = int(instance[0])))
	neural.AvgError /= len(dataset.training)
	neural.Count += 1

	#print "|", neural.AvgError, " - ", neural.PrevAvgError, "| = ", abs(neural.AvgError-neural.PrevAvgError)
	#if abs(neural.AvgError - neural.PrevAvgError) < neural.threshold:
	#	break;

	if neural.AvgError < neural.threshold:
		break;

	neural.PrevAvgError = neural.AvgError
	neural.AvgError = 0
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