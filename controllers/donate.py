import os
from lib import controller

class donate(controller.Controller):

  def index(self):
    return self.render("donate")
    
