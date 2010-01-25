import sys
import logging
import controllers
import app
import optparse
import cgi

DEFAULT_HOST = ''
DEFAULT_PORT = 9000

def handler_apache(req):
    import mod_python.util
    from mod_python import apache
    params = {}

    req.content_type = "text/html"
    route_str = req.headers_in.get("PYCHEE_END_URI","")
    if route_str:
        route_str = route_str.split(",")[0] #Hackedy hack: need to avoid ,(null) in .htaccess, this line can blow up
    form = mod_python.util.FieldStorage(req, keep_blank_values = 1)

    # Find the controller from the uri
    target_module = req.uri[1:-3].replace('/','.')
    target = target_module.split('.')[-1]
    target_module = getattr(__import__(target_module),target)
    target_cls = getattr(target_module, target)

    for fielditem in form.list:
        fieldname = fielditem.name
        fieldvalue = fielditem.value
        if getattr(fielditem, 'filename', None):
            fieldvalue = (fielditem.value,
                          fielditem.filename,
                          fielditem.type)
        params[fieldname] = fieldvalue

    # Unless you override dispatch in your controller, we hit index for / or the /method
    req.write( target_cls.dispatch(req, route_str, **params) or '' )

    return apache.OK

def handler_feather(environ, start_response):
    import feather

    params = dict(cgi.parse_qsl(environ['wsgi.input'].read()))

    url_parts = environ['PATH_INFO'].split('/')[1:]
    host_parts = environ['HTTP_Host'].split(':')[0].split('.')
    host_parts = host_parts[:-2] # TLD is known
    app_name = host_parts and host_parts[-1] or None

    cname = url_parts and url_parts[0] or ''
    mname = len(url_parts) > 1 and url_parts[1] or environ['REQUEST_METHOD'].lower()

    if app_name:
        _modname = 'apps.%s.controllers.%s' % (app_name, cname)
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
        

    response = target_cls.dispatch(environ, environ['PATH_INFO'], **params)
    start_response('200 OK', [('content-type', 'text/html'),
                              ('content_length', str(len(response)))])
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
    if options.verbose:
        logging.getLogger("feather").setLevel(logging.DEBUG)
    if options.server == "feather":
        import feather
        feather.wsgi.serve((options.host, options.port), handler_feather)
