import os
from lib import controller

class main(controller.Controller):
  ''' The hello controller greets the user '''

  def index(self):
    return self.render("main", page_name="main")
    
