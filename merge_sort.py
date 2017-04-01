from random import Random
from numpy import inf
import time

def merge_sort(items):
	if len(items) < 2:
		return items

	# split the list in two and then sort each
	split_point = int(len(items) / 2)
	sorted0 = merge_sort(items[:split_point])
	sorted1 = merge_sort(items[split_point:])
	
	# add a stopping point
	sorted0.append(inf)
	sorted1.append(inf)

	# preallocate memory for the results
	result = [None] * len(items)
	
	# merge the two lists (easy since in order)
	i0 = i1 = 0
	item0, item1 = sorted0[i0], sorted1[i1]
	for k in xrange(len(items)):
		if item0 < item1:
			result[k] = item0
			i0 += 1
			item0 = sorted0[i0]
		else:
			result[k] = item1
			i1 += 1
			item1 = sorted1[i1]
	return result

if __name__ == '__main__':
	# generate a randomly shuffled list of numbers
	nums = range(1000000)
	Random().shuffle(nums)

	start_time = time.time()
	sorted_results = merge_sort(nums)
	stop_time = time.time()

	print sorted_results
	print 'elapsed time for sort:', stop_time - start_time