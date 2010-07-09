import os
from lib import controller

class thanks(controller.Controller):

  def index(self):
    return self.render("thanks")
    
