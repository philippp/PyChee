#comment
root_dir = '/var/www/100bedsforhaiti.com/pychee'
data_dir = '%s/data' % root_dir
diskio_dir = data_dir + '/diskio'
memcache_host = '127.0.0.1:11211'
app_dir_for = lambda _app: '%s/app/%s' % (root_dir, _app)

log_dir = '%s/logs' % root_dir
log_for = lambda n : "%s/%s" % (log_dir, n)
