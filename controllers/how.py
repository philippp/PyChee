import os
from lib import controller

class how(controller.Controller):

  def index(self):
    return self.render("how")
    
