import os
from lib import controller

class twitter(controller.Controller):

  def index(self):
    return self.render("twitter")
