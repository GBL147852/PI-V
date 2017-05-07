#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import OpenGL and GLFW for visualization
import glfw
from OpenGL.GL import *

width = 512
height = 512
ratio = 1
window = None

# draw matrix
def drawMatrix(matrix):

	# start matrix projection to map glView to window size
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-ratio, ratio, -1.0, 1.0, 1.0, -1.0)
	glMatrixMode(GL_MODELVIEW)

	# start model view where vertices, edges and polygons are drawn
	glLoadIdentity()
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	# make color squares proportional to screen size based on number of columns and lines
	sizeX = 2.0 / len(matrix[0])
	sizeY = 2.0 / len(matrix)

	# start drawing colored triangles
	for j,line in enumerate(matrix):
		for i,pixel in enumerate(line):

			glBegin(GL_TRIANGLE_STRIP)

			glColor4f(pixel[0]/255,pixel[1]/255,pixel[2]/255,1)

			glVertex2f(-1 + sizeX*(j), -1 + sizeY*i)
			glVertex2f(-1 + sizeX*(j), -1 + sizeY*(i+1))
			glVertex2f(-1 + sizeX*((j+1)), -1 + sizeY*i)
			glVertex2f(-1 + sizeX*((j+1)), -1 + sizeY*(i+1))

			glEnd()

#inicializa a janela
def start():
	global window
	global width
	global height
	global ratio

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

#verifica se o loop da janela tá acontecendo sla
def loop():
	global window
	global width
	global height
	global ratio
	
	if not glfw.window_should_close(window):
		width = glfw.get_framebuffer_size(window)[0] # get current width
		height = glfw.get_framebuffer_size(window)[1] # get current height
		ratio = float(width) / height # set current screen ratio
		
		# Render here, e.g. using pyOpenGL
		glViewport(0, 0, width, height)
		glClear(GL_COLOR_BUFFER_BIT)
		
		return True
	return False
		
	
#chamado no fim de todo frame pra desenhar etc
def frameEnd():

	# Swap front and back buffers
	glfw.swap_buffers(window)

	# Poll for and process events
	glfw.poll_events()
	
#cabo
def end():
	glfw.terminate()
	