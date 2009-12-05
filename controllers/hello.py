from controllers import controller

class hello(controller.Controller):
  ''' The hello controller greets the user '''

  def index(self, who=''):
    return self.render(view="hello.index", who=who)

  def comment(self, author='anonymous', message=''):
    self.disk.write({'author':author, 'message':message},category='comment')
    return self.success()

  def comments(self):
    comment_data = self.disk.list(category='comment')
    return self.success(response = comment_data.values())
