from mpi4py import MPI
communicator = MPI.COMM_WORLD

me = communicator.rank

messages = ['from %d to %d' % (me, u)
            for u in xrange(communicator.size)]

received_messages = communicator.alltoall(messages)

print '\t'.join(received_messages)
