from mpi4py import MPI

communicator = MPI.COMM_WORLD

print 'Hello, I am %d of %d' % (communicator.rank, communicator.size)
communicator.barrier()
print 'Goodbye from %d' % communicator.rank