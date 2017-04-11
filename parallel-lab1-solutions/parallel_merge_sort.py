from random import Random
from numpy import inf
import time
import sys
import multiprocessing

def _merge_sort(items):
    if len(items) < 2:
        return items

    # split the list in two and then sort each
    split_point = int(len(items) / 2)
    sorted0 = _merge_sort(items[:split_point])
    sorted1 = _merge_sort(items[split_point:])
    
    return do_merge(sorted0, sorted1)

def do_merge(sorted0, sorted1):
    num = len(sorted0) + len(sorted1)

    # add a stopping point
    sorted0.append(inf)
    sorted1.append(inf)

    # preallocate memory for the results
    result = [None] * num
    # merge the two lists (easy since in order)
    i0 = i1 = 0
    item0, item1 = sorted0[i0], sorted1[i1]
    for k in xrange(num):
        if item0 < item1:
            result[k] = item0
            i0 += 1
            item0 = sorted0[i0]
        else:
            result[k] = item1
            i1 += 1
            item1 = sorted1[i1]
    return result

def do_merge2(twoitems):
    return do_merge(twoitems[0], twoitems[1])

def multi_merge(sorted_lists):
    while len(sorted_lists) > 1:
        pairs = [sorted_lists[i : i + 2] for i in xrange(0, len(sorted_lists), 2)]
        if len(sorted_lists) % 2 == 0:
            # i.e. this case when everything can be paired up nicely
            sorted_lists = process_pool.map(do_merge2, pairs)
        else:
            temp = process_pool.map(do_merge2, pairs[:-1])
            temp.append(sorted_lists[-1])
            sorted_lists = temp
    return sorted_lists[0]


def merge_sort(items):
    if len(items) < num_processes:
        return _merge_sort(items)
    len_sublist = int(len(items) / num_processes)
    sublists = [items[i * len_sublist : (i + 1) * len_sublist] for i in xrange(num_processes)]
    # make sure the last sublist goes all the way to the end (needed in case division has a remainder)
    sublists[-1] = items[len_sublist * (num_processes - 1) :]
    sorted_sublists = process_pool.map(_merge_sort, sublists)
    return multi_merge(sorted_sublists)


if __name__ == '__main__':
    try:
        num_processes = int(sys.argv[1])
    except:
        print 'Usage:'
        print 'python %s NUMPROCESSES' % sys.argv[0]
        sys.exit(-1)

    process_pool = multiprocessing.Pool(num_processes)

    # generate a randomly shuffled list of numbers
    nums = range(1000000)
    Random().shuffle(nums)

    start_time = time.time()
    sorted_results = merge_sort(nums)
    stop_time = time.time()

    print sorted_results
    print 'elapsed time for sort:', stop_time - start_time