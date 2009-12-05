'''
Super simple object storage mechanism.
Stores pickle-able data to the data directory and return an ID.

TODO: Semaphores to avoid write contention over the same file

TODO: Support indexing and search:
        Define data subclass that generates a hash for indexable K-V pairs.
        Include this hash in the name and use it for lookup / return.
'''
import os
import cPickle

C_LEN = 8 #Category Length

def write(data, category=0):
    
    # need semaphore, get it / TODO
    c = '0' * (C_LEN - len(str(category))) + str(category)
    cdir = 'data/%s' % c
    if not os.access(cdir,os.R_OK): #Todo: Check to existence vs. perms
        os.mkdir(cdir)
    id = len(os.listdir(cdir)) + 1    
    f = open('%s/%s' % (cdir, id), 'w')
    cPickle.dump(data, f)
    f.close()
    # release semaphore
    return id

def read(id, category=0):
    f = open('data/%s/%s' % (category, id), 'r')
    return cPickle.load(f)
