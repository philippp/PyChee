import os
from lib import controller

class partners(controller.Controller):
  ''' The hello controller greets the user '''

  def index(self):
    return self.render("partners")
    
