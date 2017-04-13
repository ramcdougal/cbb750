from mpi4py import MPI
communicator = MPI.COMM_WORLD

me_squared = communicator.rank ** 2

sum_squares = communicator.allreduce(me_squared, op=MPI.SUM)

print 'Rank %d here: sum of squares from 0 to %d is: %d' % (communicator.rank, communicator.size - 1, sum_squares)