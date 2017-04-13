from mpi4py import MPI

communicator = MPI.COMM_WORLD
me = communicator.rank

# in practice, we would want a more complicated calculation on each rank
mesquared = me * me

for i in xrange(communicator.size):
	communicator.barrier()
	if i == me:
		with open('test12.txt', 'w' if i == 0 else 'a') as f:
			f.write('%d * %d = %d\n' % (me, me, mesquared))
