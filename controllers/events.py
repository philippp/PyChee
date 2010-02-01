import os
from lib import controller

class events(controller.Controller):

  def index(self):
    return self.render("events")
