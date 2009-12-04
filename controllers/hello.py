from controllers import controller
import flickr

class hello(controller.Controller):
  ''' The hello controller greets the user '''

  def index(self, who=''):
    return self.render(view="hello.index", who=who)
