from lib import controller
from lib import cursor
from app import comments

class contact(controller.Controller):

  def index(self):
    return self.render("contact")
    
  def signup(self, name, email):
    cursor.insert('signups', name=name, email=email)
    
  def comment(self, name, email, message):
    messages.create(name, email, message)
