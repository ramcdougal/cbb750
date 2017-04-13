from mpi4py import MPI
communicator = MPI.COMM_WORLD

data = communicator.rank ** 2

if communicator.rank % 2 == 0:
	if communicator.rank < communicator.size - 1:
		communicator.send(data, dest=communicator.rank + 1)	
	if communicator.rank > 0:
		received = communicator.recv(source=communicator.rank - 1)
else:
	received = communicator.recv(source=communicator.rank - 1)
	if communicator.rank < communicator.size - 1:
		communicator.send(data, dest=communicator.rank + 1)	

if communicator.rank > 0:
	print 'Rank %d received: %d' % (communicator.rank, received)
