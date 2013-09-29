import multiprocessing


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def multiproc(l, num_proc, func, *args):
    pool = multiprocessing.Pool(processes=num_proc)

    cl = chunks(l, len(l) / num_proc)
    if args:
        cl = [(p) + args for p in cl]

    res = pool.map(func, cl)
    return [item for sublist in res for item in sublist]
