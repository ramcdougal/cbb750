from mpi4py import MPI
communicator = MPI.COMM_WORLD

# different ranks start with different data
if communicator.rank == 0:
	my_data = {'spam': 42, 'eggs': 3.14}

# now communicate; send from rank 0 to rank 1
if communicator.rank == 0:
	communicator.send(my_data, dest=1)
elif communicator.rank == 1:
	received = communicator.recv(source=0)
	print 'Rank %d received: %r' % (communicator.rank, received)
