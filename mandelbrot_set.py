from __future__ import division
from matplotlib import pyplot
import numpy
import time

xlo = -2
ylo = -1
yhi = 1
xhi = 1
nx = 1800
ny = 1200
dx = (xhi - xlo) / nx
dy = (yhi - ylo) / ny

iter_limit = 200
set_threshold = 2

def point_in_set(x, y):
	z = 0
	c = x + y * 1j
	for i in xrange(iter_limit):
		z = z ** 2 + c
		if abs(z) > set_threshold:
			return False
	return True

def calculate_set():
	result = numpy.zeros([ny, nx])
	for i in xrange(ny):
		y = i * dy + ylo
		for j in xrange(nx):
			x = j * dx + xlo
			result[i, j] = 1 if point_in_set(x, y) else 0
	return result

if __name__ == '__main__':
	start_time = time.time()
	mandelbrot_set = calculate_set()
	stop_time = time.time()
	print 'Calculation took', stop_time - start_time, 'seconds'
	pyplot.imshow(mandelbrot_set, interpolation='nearest', cmap='Greys')
	pyplot.axis('off')
	pyplot.show()