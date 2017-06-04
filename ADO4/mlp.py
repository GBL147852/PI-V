#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import csv
import os
import src.MyLittlePony as mlp
import time
import datetime



dataset = mlp.Dataset()
dataset.loadCsv(name = 'times', classes = 97)
dataset.setTrainingAndTesting()
neural = mlp.NeuralNetwork(inputNumber = dataset.inputs, classes = dataset.classes, hiddenLayers = 2, hiddenNeurons = int(math.ceil(math.sqrt(dataset.inputs*dataset.classes))))

if os.path.isfile(dataset.path+'training.csv'):
	haveTrainingFile = True
	print "Ja existe um treinamento para este dataset. Quer treinar novamente? y/n"
	if raw_input() == 'y':
		haveTrainingFile = False
else:
	haveTrainingFile = False

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
if not haveTrainingFile:
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

		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
		print '[', st, ']', neural.avgError
		#if abs(neural.AvgError - neural.PrevAvgError) < neural.threshold:
		#	break;

		if neural.avgError < neural.threshold or neural.count > 10:
			break;

		# neural.prevAvgError = neural.avgError
		neural.avgError = 0

	print 'Treinado! Construindo CSV...'

	with open("data/"+dataset.name+"/training.csv","wb") as csvfile:
		writer = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL)
		for connection in neural.connections:
			writer.writerow([connection.i,connection.j])
			writer.writerows(connection.weights)
	print 'CSV de treinamento construido!'
else:
	neural.loadTraining(trainingPath = dataset.path+'training.csv')
	print 'CSV de treinamento carregado!'
    		

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