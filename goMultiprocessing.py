import numpy as np
from time import time
from multiprocessing import Pool
import os
import sys
import pickle
import pprint
import multiprocessing as mp
import psutil
import tqdm

def listener_save(q, filelists):
    '''listens for messages on the q, writes to file. '''
    filelists_open = [open(file, 'wb') for file in filelists] #Open the files
    while 1:
        m = q.get()
        if m == 'kill':
            break
        for i,fileopen in enumerate(filelists_open):
            pickle.dump(m[1][i], fileopen)
            fileopen.flush() #Clears internal buffer to free up memory
    for fileopen in filelists_open:
        fileopen.close()

def worker_appendsave(func,L,i, seed, args,q, **kwargs):
    np.random.seed(seed+i) #In case func is using any random number generation, this is needed so that the different processes dont generate the same random number
    out = func(args, **kwargs) #Evaluate func
    for resultindex in range(len(L)):
        L[resultindex][i] = out[resultindex] #we do not use append as the proccesses are running asynchronously
    q.put([args,out[len(L):]]) #Put the func output to queue
    del out #Not sure if this is needed

def Multiprocessthis_appendsave(func, arguementlist, appendlists, filelists, seed=123, npool=0.75, **kwargs):
    '''
    Same as a for loop but using multiprocessing

    Parameters:
        func: function
                The function that needs to be run multiple times. the function should return a list of objects. The len of the array that this func returns should be len(appendedlists)+len(filelists)
        arguementlsit: list of lists
                list of arguements for which the func needs to be run
        appendlists: list of lists
                the lists where you want to append your function results
        filelists: list of strings
                the lists of file names as strings where you want to store your results
        seed: int
                In case the func uses some random number generator, this makes sure the data is reproduceable
        npool: float or int
                How many cores to use. If it is a int, use that many cores. If it is a float, use that fraction of total cores in the machine.

    Returns:
        appendedlists: list of lists
                The appended lists
    '''
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    appendlists = [np.append(appendlist,[[None]*len(arguementlist)]) for appendlist in appendlists] #since the processes will be running asynchronously, we will be using the index to update our lists instead of append
    L = [manager.list(appendlist) for appendlist in appendlists] #So that the lists are available for all child processes
    q = manager.Queue()    
    # pool = mp.Pool(mp.cpu_count() + 2)
    if type(npool)==float:
        pool = mp.Pool(int(mp.cpu_count()*npool))
    elif type(npool)==int:
        pool = mp.Pool(npool)
    else:
        raise Exception("npool must be either int or float")
    print(f'{pool} cores being opened')

    #put listener to work first
    watcher = pool.apply_async(listener_save, (q,filelists))

    #fire off workers
    jobs = []
    for i in range(len(arguementlist)):
        job = pool.apply_async(worker_appendsave, (func,L,i,seed,arguementlist[i],q), kwds=kwargs)
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in tqdm.tqdm(jobs): 
        job.get()

    #now we are done, kill the listener
    q.put('kill')
    pool.close()
    pool.join()
    return [list(l) for l in L] #converting manager list into list and returning
