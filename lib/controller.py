import config
import json

from lib import diskio, memcache

class Controller(object):
    
    #Usage: disk.write, disk.read, disk.list
    disk = diskio

    def __init__(self, *args, **kwargs):
        self.mem = memcache.Client([config.memcache_host])
        self.disk = diskio
        super(Controller, self).__init__(*args, **kwargs)

    def render(self, view, **kwargs):
        """
        Render the template specified by view as a string. Template variables
        are specified as kwargs.
        view is the package name of the template: hello.index for views/hello/index.py
        """

        # We parse out periods to support nested modules within templates.
        target = "views.%s" % view
        if 'app' in kwargs:
            target = "app.%s.%s" % (kwargs['app'], target)
            del kwargs['app']

        components = target.split('.')
        mod = __import__(target)
        for comp in components[1:]:
            mod = getattr(mod, comp)

        # Cheetah guarantees that the template class is named the same as the template module.
        tmpl = getattr(mod, components[-1])()
        [setattr(tmpl, k, v) for k,v in kwargs.items()]
        return str(tmpl)

    def success(self, response=True):
        """JSON-format success response"""
        return json.dumps({'c':0, 'data':response})

    def failure(self, response=False, code=1):
        """JSON-format failure response"""
        return json.dumps({'c':code, 'data':response})

    @classmethod
    def dispatch(cls, req, method, **kwargs):
        """
        Routing dispatcher, triggers any and all controller activity.
        Override this method to change the path-to-method resolution or 
        to manipulate arguments. 
        The default resolves /foo/bar to method "bar" on controller "foo"
        """

        controller_obj = cls()
        if method and not getattr(controller_obj, method, None):
            method = req['PATH_INFO']
        if method and getattr(controller_obj, method ,None):
            return getattr(controller_obj, method)(**kwargs) 
        else:
            return controller_obj.index(**kwargs)
