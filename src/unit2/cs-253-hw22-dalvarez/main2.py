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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
#import re

form = """
<h1>Signup</h1>
<form method="post" action="/signup">
  <label>
    Username
    <input type="text" name="username" value="%(username)s">
  </label>
  <br>
  <label>
    Password
    <input type="password" name="password" value="%(password)s">
  </label>
  <br>
  <label>
    Verify Password
    <input type="password" name="verify" value="%(verify)s" >
  </label>
  <br>
  <label>
    Email (optional)
    <input type="text" name="email" value="%(email)s">
  </label>
  <br>
  <input type="submit">
</form>
"""

class MainHandler(webapp.RequestHandler):
    def write_form(self, error="", username="", password="", verify="", email=""):
        self.response.headers['Content-Type'] = 'text/html'
        #self.response.out.write(form %{"error": error, "username": username, "password": password, "verify": verify, "email": email})
        self.response.out.write(form)

    def get(self):
        self.write_form()

class SignupHandler(webapp.RequestHandler):

    #def valid_username(username):
    #    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    #    return user_re.match(username)

    def get(self):
        self.response.out.write("get")

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        #username = valid_username(username)

        #if not(username):
        #  self.write_form("That doesn’t look valid to me, friend.", username)
        #else:
        #  self.response.out.write("Thanks! That’s a totally valid day!")
        self.response.out.write("Thanks! That’s a totally valid day!")


def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/signup', SignupHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()