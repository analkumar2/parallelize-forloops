import numpy as np
from time import time
from multiprocessing import Pool
import os
import sys
import pickle
import pprint
import multiprocessing as mp

def worker_append(func,L,args):
    np.random.seed(args[0])
    out = func(args[1:])
    for i in range(len(out)):
        L[i].append(out[i])

def worker_save(func,args,q):
    np.random.seed(args[0])
    out = func(args[1:])
    q.put([args,out])
    return [args,out]

def listener_append(q):
    '''listens for messages on the q. '''
    outlist = []
    while 1:
        m = q.get()
        if m == 'kill':
            break
        outlist.append(m[1])
        print(m[0])
    return outlist

def listener_save(q):
    '''listens for messages on the q, writes to file. '''

    with open(fn, 'ab') as f:
        while 1:
            m = q.get()
            if m == 'kill':
                break
            print(m[0])
            pickle.dump(m[1], f)

def Multiprocessthis_append(func, arguementlist, appendlists, seed=123):
    manager = mp.Manager()
    L = [manager.list(appendlist) for appendlist in appendlists]   
    pool = mp.Pool(mp.cpu_count() + 2)

    #fire off workers
    jobs = []
    for i in range(len(arguementlist)):
        job = pool.apply_async(worker_append, (func,L,np.append(seed+i,arguementlist[i])))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs: 
        job.get()

    pool.close()
    pool.join()
    return [list(l) for l in L]

def Multiprocessthis_save(func, arguementlist, filelists, seed=123):
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(mp.cpu_count() + 2)

    #put listener to work first
    watcher = pool.apply_async(listener, (q,))

    #fire off workers
    jobs = []
    for i in range(1000):
        job = pool.apply_async(worker, (i,q))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs: 
        job.get()

    #now we are done, kill the listener
    q.put('kill')
    pool.close()
    pool.join()