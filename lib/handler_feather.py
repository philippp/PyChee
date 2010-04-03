import feather
import optparse
import cgi

import pdb
import logging
import logging.handlers
import feather
import config
import lib.fails

DEFAULT_HOST = ''
DEFAULT_PORT = 9000
FEATHER_LOG_FILENAME = config.log_for('feather')

def handler(environ, start_response):
    params = {}
    if environ['REQUEST_METHOD'] == 'POST':
        params = eval_form_data(environ)
    
    if 'QUERY_STRING' in environ:
        get_params = dict([ p.split("=") for p in environ['QUERY_STRING'].split('&') ])
        params.update( get_params )

    url_parts = filter(lambda p : bool(p),
                       environ['PATH_INFO'].split('/')[1:])
    host_parts = environ['HTTP_Host'].split(':')[0].split('.')
    host_parts = host_parts[:-2] # TLD is known
    app_name = host_parts and host_parts[-1] or None
    cname = url_parts and url_parts[0] or ''
    method = len(url_parts) > 1 and url_parts[1] or ''
    try:
        mime, response = eval_controller(environ, start_response, cname, 
                                         method, params, app_name=app_name)
        if not response:
            if not url_parts: 
                url_parts = ['index.html']
            mime, response = eval_static(url_parts, app_name=app_name)
            if not response:
                return feather_404(start_response, msg='file not found')

        start_response('200 OK', [('content-type', mime),
                                  ('content_length', str(len(response)))])
        return [response]
    except Exception, e:
        start_response('200 OK', [('content-type', mime),
                                  ('content_length', str(len(str(e))))])    
        return [str(e)]

def eval_form_data(environ):
    raw_body = environ['wsgi.input'].read()
    params = dict(cgi.parse_qsl(environ['wsgi.input'].read()))
    return {}

def eval_controller(environ, start_response, cname, method, params, app_name=''):

    cname = cname or '_root'
    if app_name:
        _modname = 'app.%s.controllers.%s' % (app_name, cname)
    else:
        _modname = 'controllers.%s' % (cname)

    try:
        cmodule = __import__(_modname,
                             fromlist = [cname],
                             globals=globals(),
                             locals=locals())
        target_cls = getattr(cmodule, cname, None)
        if not target_cls:
            return None, None
    except ImportError, e:
        return None, None
        
    response = target_cls.dispatch(environ, method, **params)
    return 'text/html', response

def eval_static(url_parts, app_name=None):
    '''
    open the file, return the contents
    '''

    fext = url_parts[-1].split(".")[-1]

    fpath_s =  '/static/' + "/".join(url_parts)

    if app_name:
        try:
            app_dir = config.app_dir_for(app_name)
            fc = file(app_dir+fpath_s).read()
            return FILE_MIMETYPE[fext], fc
        except IOError, e:
            pass
    try:
        fc = file(config.root_dir+fpath_s).read()
        return FILE_MIMETYPE[fext], fc
    except IOError, e:
        return None, None

FILE_MIMETYPE = {
    'js' : 'text/javascript',
    'css' : 'text/css'
    }

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
