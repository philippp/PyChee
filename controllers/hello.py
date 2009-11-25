import controllers
import flickr

class hello(controllers.controller):
  ''' The hello controller greets the user '''

  def index(self, who=''):
    return self.render(who=who)

  def goodbye(self,when=''):
    return "kthxbye"
