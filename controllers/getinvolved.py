from lib import controller
from lib import cursor
from app import comments

class getinvolved(controller.Controller):

  def index(self):
    return self.render("getinvolved")
    
  def signup(self, name, email, submit=None):
    cursor.insert('signups', name=name, email=email)
    return self.render("thanks",message="Thanks, we'll be in touch")

  def comment(self, name, email, message, submit=None):
    comments.create(name, email, message)
    return self.render("thanks",message="Thanks for getting in touch")
