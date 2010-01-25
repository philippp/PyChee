import feather
import optparse
import cgi

import pdb
import logging
import logging.handlers
import feather
import config

DEFAULT_HOST = ''
DEFAULT_PORT = 9000
FEATHER_LOG_FILENAME = config.log_for('feather')

def handler(environ, start_response):

    params = dict(cgi.parse_qsl(environ['wsgi.input'].read()))
    
    url_parts = environ['PATH_INFO'].split('/')[1:]
    host_parts = environ['HTTP_Host'].split(':')[0].split('.')
    host_parts = host_parts[:-2] # TLD is known
    app_name = host_parts and host_parts[-1] or None

    cname = url_parts and url_parts[0] or ''
    mname = len(url_parts) > 1 and url_parts[1] or environ['REQUEST_METHOD'].lower()
    
    if app_name:
        _modname = 'app.%s.controllers.%s' % (app_name, cname)
    else:
        _modname = 'controllers.%s' % (cname)

    if not cname:
        _modname = _modname[:-1]
        cname = 'controllers'

    try:
        cmod = __import__(_modname,
                          fromlist = [cname],
                          globals=globals(),
                          locals=locals())
        target_cls = getattr(cmod, cname, None)
        if not target_cls:
            return feather_404(start_response, 'controller not found')
    except ImportError, e:
        return feather_404(start_response, 'controller not found')
        
    try:
        response = target_cls.dispatch(environ, environ['PATH_INFO'], **params)
        start_response('200 OK', [('content-type', 'text/html'),
                                  ('content_length', str(len(response)))])
    except Exception, e:
        return str(e)
    return [response]

def feather_404(start_response, msg='not hurr'):
        start_response('404 NOT FOUND', [('content-type','text/html'),
                                         ('content-length', len(msg))])
        return [msg]

if __name__ == "__main__":
    parser = optparse.OptionParser(add_help_option=False)
    parser.add_option("-v", "--verbose", action="store_true")
    parser.add_option("-s", "--server", type="str", default="feather")
    parser.add_option("-p", "--port", type="int", default=DEFAULT_PORT)
    parser.add_option("-h", "--host", default=DEFAULT_HOST)

    options, args = parser.parse_args()
    flogger = logging.getLogger("feather")
    if options.verbose:
        flogger.setLevel(logging.DEBUG)

#    handler = logging.handlers.RotatingFileHandler(
#        FEATHER_LOG_FILENAME, maxBytes=1024 * 1024, backupCount=5)
#    flogger.addHandler(handler)

    feather.wsgi.serve((options.host, options.port), handler)
