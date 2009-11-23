import controllers
import flickr

class hello(controllers.controller):
  ''' The hello controller greets the user '''

  def index(self, req, who=''):
    return self.render(who=who)
