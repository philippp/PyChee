import os
from lib import controller

class main(controller.Controller):

  def index(self):
    return self.render("main")
    
