import multiprocessing




def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def get_pool(num_proc):
    return multiprocessing.Pool(processes=num_proc)


def multiproc(l, num_proc, func, pool=None, *args):
    if pool is None:
        print "No pool, making a new one"
        pool = multiprocessing.Pool(processes=num_proc)

    cl = chunks(l, len(l) / num_proc)
    if args:
        cl = [(p) + args for p in cl]

    res = pool.map(func, cl)
    return [item for sublist in res for item in sublist]
