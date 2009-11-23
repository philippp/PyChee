class controller(object):
    
    def render(self, **kwargs):
        target = self.__class__.__name__.lower()
        tmpl_module = getattr(__import__("views.%s" % target), target)
        tmpl = getattr(tmpl_module, target)()
        [setattr(tmpl, k, v) for k,v in kwargs]
        return str(tmpl)
