'''
Super simple object storage mechanism.
Stores pickle-able data to the data directory and return an ID.

TODO: Semaphores to avoid write contention over the same file
'''
import os
import cPickle
import config
from lib import logger

def write(data, category='0'):
    # need semaphore, get it / TODO
    cdir = '%s/%s' % (config.diskio_dir, category)
    if not os.access(cdir,os.R_OK): #Todo: Check to existence vs. perms
        os.mkdir(cdir)
    id = len(os.listdir(cdir)) + 1    
    f = open('%s/%s' % (cdir, id), 'w')
    cPickle.dump(data, f)
    f.close()
    # release semaphore
    return id

def read(id, category='0'):
    f = open('%s/%s/%s' % (config.diskio_dir, category, id), 'r')
    return cPickle.load(f)

def list(category='0'):
    cdir = '%s/%s' % (config.data_dir, category)
    if not os.access(cdir,os.R_OK):
        return []
    ids = [int(id) for id in os.listdir(cdir)]
    ids.sort()
    logger.write(ids)
    return [ (id, read(id, category=category)) for id in ids ]
