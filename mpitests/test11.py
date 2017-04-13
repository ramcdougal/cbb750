from mpi4py import MPI
import numpy

communicator = MPI.COMM_WORLD
assert communicator.size == 2
rank = communicator.rank
x = numpy.linspace(0, 6.28)
n = len(x)
f = [numpy.sin, numpy.cos][rank]
y = f(x)
results = numpy.zeros(n * 2, dtype='d')
communicator.Allgather([y, MPI.DOUBLE], results)
if rank == 0:
	from matplotlib import pyplot
	pyplot.plot(x, results[:n], x, results[n:])
	pyplot.xlim([min(x), max(x)])
	pyplot.show()

communicator.barrier()
