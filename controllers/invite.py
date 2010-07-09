from lib import controller

class invite(controller.Controller):

  def index(self):
    return self.render("invite")
  
