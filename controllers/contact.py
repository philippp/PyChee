from lib import controller
from lib import cursor
from app import comments

class contact(controller.Controller):

  def index(self):
    return self.render("contact")
    
  def signup(self, name, email):
    cursor.insert('signups', name=name, email=email)
    return self.render("thanks",message="Thanks, we'll be in touch")

  def comment(self, name, email, message, *args, **kwargs):
    comments.create(name, email, message)
    return self.render("thanks",message="Thanks for getting in touch")
