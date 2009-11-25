class controller(object):
    
    def render(self, **kwargs):
        target = self.__class__.__name__.lower()
        tmpl_module = getattr(__import__("views.%s" % target), target)
        tmpl = getattr(tmpl_module, target)()
        [setattr(tmpl, k, v) for k,v in kwargs.items()]
        return str(tmpl)
    
    @classmethod
    def dispatch(cls, req, uri, **kwargs):
        ''' /foo/bar will invoke method bar on controller foo '''
        controller_obj = cls()
        uri_parts = uri.split("/")
        if uri_parts and len(uri_parts) > 1 and getattr(controller_obj, uri_parts[1],None):
            return getattr(controller_obj, uri_parts[1])(**kwargs) 
        else:
            return controller_obj.index(**kwargs)
