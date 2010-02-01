import os
from lib import controller

class help(controller.Controller):

  def index(self):
    return self.render("help")
