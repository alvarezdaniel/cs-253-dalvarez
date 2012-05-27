#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext.webapp import util

import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

def escape(s):
  return cgi.escape(s, quote = True)

##def blog_key(name = 'default'):
##    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class PostPage(webapp.RequestHandler):

    def render_post(self, post=None):

        values = {
            'subject' : post.subject,
            'content' : post.content,
        }

        path = os.path.join(os.path.dirname(__file__), 'post.html')
        self.response.out.write(template.render(path, values))

    def get(self, id):

        #key = db.Key.from_path('Post', int(id), parent=blog_key())
        key = db.Key.from_path('Post', int(id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render_post(post = post)

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
            #p = Post(parent = blog_key(), subject = subject, content = content)
            p = Post(subject = subject, content = content)
            p.put()
            self.redirect('/%s' % str(p.key().id()))

        else:
            error = "we need both a subject and some content!"
            self.render_newpost(escape(subject), escape(content), escape(error))

class BlogHandler(webapp.RequestHandler):
    def render_posts(self, posts=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        values = { 'posts' : posts }

        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, values))

    def get(self):
        self.render_posts()

def main():
    application = webapp.WSGIApplication([('/', BlogHandler),
                                          ('/newpost', NewPostPage),
                                          ('/([0-9]+)', PostPage)
                                          ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
