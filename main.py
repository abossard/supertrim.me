import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template


class Weight(db.Model):
    belongs_to = db.UserProperty()
    weight = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
          weights_query = Weight.all().filter('belongs_to = ', users.get_current_user()).order('-date')
          weights = weights_query.fetch(10)
          user = users.get_current_user()
          url = users.create_logout_url(self.request.uri)
          url_linktext = 'Logout'
        else:
          user = None
          weights = None
          url = users.create_login_url(self.request.uri)
          url_linktext = 'Login'

        template_values = {
            'weights': weights,
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        

class EnterWeight(webapp.RequestHandler):
    def post(self):
        weight = Weight()
        weight.belongs_to = users.get_current_user()
        weight.weight = int(self.request.get('weight'))
        weight.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/enter_weight', EnterWeight)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
