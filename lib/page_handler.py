import sys
import controllers
from mod_python import apache

def handler(req):
    req.content_type = "text/html"
    target_module = req.uri[1:-3].replace('/','.')
    target = target_module.split('.')[-1]
    target_module = getattr(__import__(target_module),target)
    target_cls = getattr(target_module, target)
    target_obj = target_cls()
    req.write( target_obj.index(req) or '' )
    return apache.OK
