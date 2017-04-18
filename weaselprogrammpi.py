from mpi4py import MPI
communicator = MPI.COMM_WORLD

import numpy
try:
    from randomstate.prng.pcg64 import RandomState
except ImportError:
    print """Importing randomstate failed. To fix, try:
    sudo pip install randomstate"""
    import sys
    sys.exit()

gene_bases = [base for base in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ']

random_seed = 3

size_of_generation = 1000

size_of_my_generation = size_of_generation / communicator.size
start = communicator.rank * size_of_my_generation
stop = start + size_of_my_generation
if communicator.rank == communicator.size - 1:
	stop = size_of_generation

prngs = [RandomState(random_seed, i) for i in xrange(start, stop)]

def mutate(gene, prng, mutation_rate=0.05):
	copy = ''
	for base in gene:
		if prng.uniform() < mutation_rate:
			copy += prng.choice(gene_bases)
		else:
			copy += base
	return copy

def fitness(gene, reference='METHINKS IT IS LIKE A WEASEL'):
	return sum([1 for base, ref_base in zip(gene, reference) if base == ref_base])

def new_population(parent, mutation_rate=0.05):
	return [mutate(parent, prng, mutation_rate=mutation_rate) for prng in prngs]

def best_in_population(population):
	"""return the fittest individual in the population"""
	return population[numpy.argmax([fitness(individual) for individual in population])]

def get_next_parent(parent, mutation_rate=0.05):
	"""evolve a new population from the parent, and find the new fittest individual"""
	return best_in_population(new_population(parent, mutation_rate=mutation_rate))

def weasel_program(mutation_rate=0.05, initial='                            '):
	generation = 0
	score = fitness(initial)
	parent = initial
	while score < len(parent):
		if communicator.rank == 0:
			print '%3d  %s  (%d)' % (generation, parent, score)
		possible_parent = get_next_parent(parent)
		# at this point, possible_parent is only who the current rank thinks is best... needs to compare with the others
		possible_parents = communicator.allgather(possible_parent)
		parent = best_in_population(possible_parents)
		generation += 1
		score = fitness(parent)
	if communicator.rank == 0:
		print '%3d  %s  (%d)' % (generation, parent, score)

if __name__ == '__main__':
	import time
	start = time.time()
	weasel_program()
	if communicator.rank == 0:
		print 'evolution time:', time.time() - start