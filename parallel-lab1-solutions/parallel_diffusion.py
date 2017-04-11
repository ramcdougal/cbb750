from matplotlib import pyplot
import numpy
import time
import sys
import multiprocessing
try:
    from randomstate.prng.pcg64 import RandomState
except ImportError:
    print """Importing randomstate failed. To fix, try:
    sudo pip install randomstate"""
    import sys
    sys.exit()

random_seed = 1
random_stream = 1

x_lo = 0
x_hi = 200
num_molecules = 10000
molecule_locations = [100] * num_molecules

# our rule for diffusion
def advance(molecules, i_interval, store_every, advance_to):
    results = [numpy.zeros(x_hi - x_lo + 1)
               for i in xrange(1 + advance_to / store_every)]
    for i in xrange(*i_interval):
        mol_loc = molecules[i]
        # every molecule gets its own random stream
        prng = RandomState(random_seed, 1 + i)
        for t in xrange(advance_to):
            if t % store_every == 0:
                results[t / store_every][mol_loc] += 1
            r = prng.uniform()
            if r < 0.4:
                mol_loc = max(x_lo, mol_loc - 1)
            elif r < 0.8:
                mol_loc = min(x_hi, mol_loc + 1)
        molecules[i] = mol_loc

    return results

def _advance(data):
    return advance(*data)

if __name__ == '__main__':
    try:
        num_processes = int(sys.argv[1])
    except:
        print 'Usage:'
        print 'python %s NUMPROCESSES' % sys.argv[0]
        sys.exit(-1)

    pool = multiprocessing.Pool(num_processes)

    start = time.time()

    # figure out how to divide the work
    len_interval = int(num_molecules / num_processes)
    intervals = [(i * len_interval, (i + 1) * len_interval) for i in xrange(num_processes)]
    # make sure the last sublist goes all the way to the end (needed in case division has a remainder)
    intervals[-1] = (len_interval * (num_processes - 1), num_molecules)


    advance_to = 2001
    store_every = 400    
    results_lists = pool.map(_advance, [(molecule_locations, interval, store_every, advance_to) for interval in intervals])
    results = [0] * len(results_lists[0])
    for result in results_lists:
    	for j in xrange(len(results)):
    		results[j] += result[j]
    #for i in xrange(1, len(results_lists)):
    #    results += results[i]

    stop = time.time()

    for i, time_point in enumerate(results):
        pyplot.plot(time_point, label='t = %d' % (i * store_every))

    print 'simulation time:', stop - start

    pyplot.legend()
    pyplot.ylim([0, 300])
    pyplot.show()