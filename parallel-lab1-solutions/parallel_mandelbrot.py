from __future__ import division
from matplotlib import pyplot
import numpy
import time
from multiprocessing import JoinableQueue, Process
import sys

xlo = -2
ylo = -1
yhi = 1
xhi = 0.5
nx = 200
ny = 160
dx = (xhi - xlo) / nx
dy = (yhi - ylo) / ny

iter_limit = 500
set_threshold = 2

def point_in_set(x, y):
    z = 0
    c = x + y * 1j
    for i in xrange(iter_limit):
        z = z ** 2 + c
        if abs(z) > set_threshold:
            return False
    return True

def worker(todo_queue, results_queue):
    while True:
        x, y, i, j = todo_queue.get()
        val = 1 if point_in_set(x, y) else 0
        results_queue.put((i, j, val))
        todo_queue.task_done()

def calculate_set(num_processes):
    todo_queue = JoinableQueue()
    results_queue = JoinableQueue()

    # setup and launch workers
    # we'll make them daemon processes so they shut down automatically when this process exits, but
    # we'll also shut them down ourselves when we finish
    workers = [Process(target=worker, args=(todo_queue, results_queue)) for i in xrange(num_processes)]
    for individual in workers:
        individual.daemon = True
        individual.start()

    result = numpy.zeros([ny, nx])
    for i in xrange(ny):
        y = i * dy + ylo
        for j in xrange(nx):
            x = j * dx + xlo
            todo_queue.put((x, y, i, j))
    todo_queue.join()

    while not results_queue.empty():
        i, j, val = results_queue.get()
        result[i, j] = val
        results_queue.task_done()

    # shutdown the compute processes
    for individual in workers:
        individual.terminate()

    return result

if __name__ == '__main__':
    try:
        num_processes = int(sys.argv[1])
    except:
        print 'Usage:'
        print 'python %s NUMPROCESSES' % sys.argv[0]
        sys.exit(-1)

    start_time = time.time()
    mandelbrot_set = calculate_set(num_processes)
    stop_time = time.time()
    print 'Calculation took', stop_time - start_time, 'seconds'
    pyplot.imshow(mandelbrot_set, interpolation='nearest', cmap='Greys')
    pyplot.axis('off')
    pyplot.show()