import os
import webapp2
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(webapp2.RequestHandler):

    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

        values = {
            'title': title,
            'art': art,
            'error': error,
            'arts' : arts
        }

        path = os.path.join(os.path.dirname(__file__), 'front.html')
        self.response.out.write(template.render(path, values))

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            a.put()
            self.redirect("/")

        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)

def main():
    application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
