import os
from lib import controller
from lib import cursor
from app import comments
from app import signups

class admin(controller.Controller):

  def index(self):
    return self.render("main")
    

  def console(self):
    comm = comments.get()
    sign = signups.get()
    return self.render("admin",
                       comments = comm,
                       signups = sign)
