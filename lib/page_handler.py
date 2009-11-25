import sys
import controllers
import mod_python.util
from mod_python import apache

def handler(req):
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

    # GET/POST params
    params =  dict([(fielditem.name, fielditem.value) for fielditem in form.list])

    # Unless you override dispatch in your controller, we hit index for / or the /method
    req.write( target_cls.dispatch(req, route_str, **params) or '' )

    return apache.OK
