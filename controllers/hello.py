from lib import controller

class hello(controller.Controller):
  ''' The hello controller greets the user '''

  def index(self, author='', message=''):
    if author and message:
      self.disk.write({'author':author, 'message':message},category='comment')  
    comment_data = [data for id, data in self.disk.list(category='comment')]
    return self.render("hello.index", comment_data=comment_data)
