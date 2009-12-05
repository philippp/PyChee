import json
from lib import diskio

class Controller(object):
    
    #Usage: disk.write, disk.read, disk.list
    disk = diskio

    def render(self, **kwargs):
        target = kwargs.get('view',None)
        if target:
            del kwargs['view']
        else:
            target = self.__class__.__name__.lower()
        
        # We parse out periods to support nested modules within templates.
        target = "views.%s" % target
        components = target.split('.')
        mod = __import__(target)
        for comp in components[1:]:
            mod = getattr(mod, comp)

        # Cheetah guarantees that the template class is named the same as the template module.
        tmpl = getattr(mod, components[-1])()
        [setattr(tmpl, k, v) for k,v in kwargs.items()]
        return str(tmpl)

    def success(self, response=True):
        return json.dumps({'c':0, 'data':response})

    def failure(self, response=False, code=1):
        return json.dumps({'c':code, 'data':response})

    @classmethod
    def dispatch(cls, req, uri, **kwargs):
        ''' Routing dispatcher, triggers any and all controller activity.
        /foo/bar will invoke method bar on controller foo.
        '''
        controller_obj = cls()
        uri_parts = uri.split("/")
        if uri_parts and len(uri_parts) > 1 and getattr(controller_obj, uri_parts[1],None):
            return getattr(controller_obj, uri_parts[1])(**kwargs) 
        else:
            return controller_obj.index(**kwargs)
