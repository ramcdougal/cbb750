from mpi4py import MPI

communicator = MPI.COMM_WORLD
me = communicator.rank

# in practice, we would want a more complicated calculation on each rank
mesquared = me * me

for i in xrange(communicator.size):
	communicator.barrier()
	if i == me:
		print('%d * %d = %d' % (me, me, mesquared))
