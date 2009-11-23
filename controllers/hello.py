import controllers
import flickr

class hello(controllers.controller):
  ''' The hello controller greets the user '''

  def index(self, req, who='stranger'):
    return self.render(who=who)
