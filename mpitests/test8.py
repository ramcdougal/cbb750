from mpi4py import MPI
communicator = MPI.COMM_WORLD

me_squared = communicator.rank ** 2

all_squares = communicator.allgather(me_squared)

print 'Rank %d here, and here are squares:\n%r' % (communicator.rank, all_squares)