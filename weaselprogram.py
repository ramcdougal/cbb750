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
prngs = [RandomState(random_seed, i) for i in xrange(size_of_generation)]

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
		print '%3d  %s  (%d)' % (generation, parent, score)
		parent = get_next_parent(parent)
		generation += 1
		score = fitness(parent)
	print '%3d  %s  (%d)' % (generation, parent, score)

if __name__ == '__main__':
	weasel_program()