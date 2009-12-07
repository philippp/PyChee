import config
import time

def write(msg, category='0'):
    # need semaphore, get it / TODO
    f = open("%s/pychee.log" % config.log_dir, 'a')
    f.write("[%s][%s]%s" % (category, time.ctime(), msg))
    f.close()
