import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

def escape(s):
  return cgi.escape(s, quote = True)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class PostPage(webapp.RequestHandler):

##    def render_post(self, subject="", content=""):
##        values = {
##            'subject' : subject,
##            'content' : content,
##        }
##
##        path = os.path.join(os.path.dirname(__file__), 'post.html')
##        self.response.out.write(template.render(path, values))

    def get(self):
        #subject = self.request.get("subject")
        #content = self.request.get("content")
        #self.render_post(subject, content)
        self.reponse.out.write("Hola")

class NewPostPage(webapp.RequestHandler):

    def render_newpost(self, subject="", content="", error=""):
        values = {
            'subject' : subject,
            'content' : content,
            'error': error
        }

        path = os.path.join(os.path.dirname(__file__), 'newpost.html')
        self.response.out.write(template.render(path, values))

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(subject = subject, content = content)
            p.put()
            self.redirect('/post/%s' % str(p.key().id()))

        else:
            error = "we need both a subject and some content!"
            self.render_newpost(escape(subject), escape(content), escape(error))

class MainPage(webapp.RequestHandler):

    def render_posts(self, posts=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        values = { 'posts' : posts }

        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, values))

    def get(self):
        self.render_posts()

def main():
    application = webapp.WSGIApplication([('/', MainPage), ('/newpost', NewPostPage), ('/post/14', PostPage)], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
