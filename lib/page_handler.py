import sys
import controllers
import mod_python.util
from mod_python import apache

def handler(req):
    req.content_type = "text/html"
    route_str = (req.headers_in.get("PYCHEE_END_URI",""))
    if route_str:
        route_str = route_str.split(",")[0] #Hackedy hack: need to avoid ,(null) in .htaccess, this line can blow up
    form = mod_python.util.FieldStorage(req, keep_blank_values = 1)
    target_module = req.uri[1:-3].replace('/','.')
    target = target_module.split('.')[-1]
    target_module = getattr(__import__(target_module),target)
    target_cls = getattr(target_module, target)
    target_obj = target_cls()
    params =  dict([(fielditem.name, fielditem.value) for fielditem in form.list])
    req.write( target_obj.index(req, **params) or '' )
    return apache.OK
