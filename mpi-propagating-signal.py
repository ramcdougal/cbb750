from mpi4py import MPI
communicator = MPI.COMM_WORLD

from matplotlib import pyplot
import itertools
import time
import numpy

def init_process(y_to_share, new_y_to_share):
	global y, new_y
	y = y_to_share
	new_y = new_y_to_share

# our rule for reaction-diffusion
def advance(dt, start_i, stop_i):
    n = len(y)
    for j in xrange(start_i, stop_i):
        new_y[j] = y[j] + dt * (20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % n])
                           - y[j] * (1 - y[j]) * (0.3 - y[j]))


if __name__ == '__main__':
    # initial conditions
    y = numpy.zeros(1000)
    new_y = numpy.zeros(len(y))
    y[480:520] = [1] * 40

    # figure out how to divide the work
    size_of_each = len(y) / communicator.size
    start_i = communicator.rank * size_of_each
    stop_i = start_i + size_of_each
    if communicator.rank == communicator.size - 1:
        stop_i = len(y)

    start = time.time()
    # time-step
    dt = 0.01

    # advance through t (t = i * dt) is at least 100; plot
    # every 20
    i = 0
    while i * dt <= 100:
        if i * dt % 20 == 0:
            # to plot, rank 0 really does need all the data
            my_y = list(y[start_i:stop_i])
            # could do an allgather here, but slightly more efficient to do a gather and only send to rank 0
            data = communicator.gather(my_y, root=0)
            if communicator.rank == 0:
                y[:] = list(itertools.chain.from_iterable(data))
                pyplot.plot(y, label='t = %g' % (i * dt))

        advance(dt, start_i, stop_i)

        # now share the boundaries with the other nodes (in principle, this doesn't need to be an allgather, but simplest)
        boundary_data = {start_i: new_y[start_i], stop_i - 1: new_y[stop_i - 1]}
        all_boundary_data = communicator.allgather(boundary_data)
        for rank_data in all_boundary_data:
            for index, val in rank_data.iteritems():
                new_y[index] = val

        # update y to the new value and repeat
        y[:] = new_y[:]
        i += 1
        if communicator.rank == 0:
            print i * dt

    if communicator.rank == 0:
        print 'compute time:', time.time() - start
        pyplot.legend()
        pyplot.show()

    communicator.barrier()