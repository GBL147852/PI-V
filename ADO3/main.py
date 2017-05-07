#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import random
import stuff as s
import reader

# import OpenGL and GLFW for visualization
import glfw
from OpenGL.GL import *

# draw matrix
def drawMatrix(lines, columns, ratio):

	# start matrix projection to map glView to window size
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-ratio, ratio, -1.0, 1.0, 1.0, -1.0)
	glMatrixMode(GL_MODELVIEW)

	# start model view where vertices, edges and polygons are drawn
	glLoadIdentity()
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	# make color squares proportional to screen size based on number of columns and lines
	sizeX = 2.0 / columns
	sizeY = 2.0 / lines

	# start drawing colored triangles
	for i in range(lines):
	    for j in range(columns):

	        glBegin(GL_TRIANGLE_STRIP)

	        glColor4f(1, 1, 1, 1)

	        glVertex2f(-1 + sizeX*(j), -1 + sizeY*i)
	        glVertex2f(-1 + sizeX*(j), -1 + sizeY*(i+1))
	        glVertex2f(-1 + sizeX*((j+1)), -1 + sizeY*i)
	        glVertex2f(-1 + sizeX*((j+1)), -1 + sizeY*(i+1))

	        glEnd()

#parte 1 do projeto
def parte1():
	print "parte 1!"

	#inicializa o filho
	som = s.Som(3,0,255)
	entradas = [
		[255,0	,0	],
		[255,255,0	],
		[0	,255,0	],
		[0	,255,255],
		[0	,0	,255],
		[255,0	,255],
	]

	#treina ele
	print "treinando!!", som.iteracoes, "iterações..."
	n = 0
	for i in xrange(som.iteracoes):
		som.atualizarPesos(entradas[n])
		n = (n+1)%len(entradas)

	#ae
	print "foi!!"
	print "coisos encontrados pras entradas:\n"
	for i in entradas:
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio vencedor:", valor[0], "x", valor[1], "\n"

	#falta plotar isso!

#parte 2 do projeto
def parte2():
	print "parte 2!"

#	dataset = "breast"
	dataset = "iris"
#	dataset = "wine"

	print "dataset:", dataset

	#carrega dataset
	dataLen,entradas,classes = reader.load(dataset)

	#atribui as cores abaixo às classes
	coresPossiveis = [
		[255,0,0],
		[0,255,0],
		[0,0,255],
	]
	corIndex = 0
	cores = {}
	for i in classes:
		if i not in cores:
			cores[i] = coresPossiveis[corIndex]
			corIndex += 1

	#inicializa e treina o guri
	som = s.Som(len(entradas[0])-1,0,1)
	print "treinando!!", som.iteracoes, "iterações..."
	n = 0
	for i in xrange(som.iteracoes):
		som.atualizarPesos(entradas[n][1:])
		n = (n+1)%len(entradas)

	#ae
	print "foi!!"
	print "coisos encontrados pras entradas:\n"
	for n,i in enumerate(entradas):
		valor = som.obterNeuronioVencedor(i)
		print "entradas:", "%.5f " * len(i) % tuple(i)
		print "neurônio vencedor:", valor[0], "x", valor[1], "\n"
		cor = cores[classes[n]]
		#neurônio em (valor[0],valor[1]) recebe a cor acima!
		#(quando estiver plotando etc)

#Função principal
def main():

	# initial values of width and height of the glfw window
	width = 640
	height = 480

	# Initialize glfw
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(width, height, "SOM result viewer", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glClearColor(0, 0, 0, 0);

    # parte1()
	parte2()
	raw_input()

	# Loop until the user closes the window
	while not glfw.window_should_close(window):

	    width = glfw.get_framebuffer_size(window)[0] # get current width
	    height = glfw.get_framebuffer_size(window)[1] # get current height
	    ratio = float(width) / height # set current screen ratio

	    # Render here, e.g. using pyOpenGL
	    glViewport(0, 0, width, height)
	    glClear(GL_COLOR_BUFFER_BIT)

		# Start drawing matrix
		drawMatrix(lines, columns, ratio)

		# Swap front and back buffers
        glfw.swap_buffers(window)

	    # Poll for and process events
        glfw.poll_events()

	glfw.terminate()

main()
