import os
from lib import controller

class about(controller.Controller):

  def index(self):
    return self.render("about")
    
