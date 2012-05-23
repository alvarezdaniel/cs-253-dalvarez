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
import cgi

form = """
<h1>Signup</h1>
<form method="post" action="/">
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
  <div style="color: red">%(error)s</div>
  <br>
  <input type="submit">
</form>
"""

def escape(s):
  return cgi.escape(s, quote = True)

class SignupHandler(webapp.RequestHandler):

    def write_form(self, error="", username="", password="", verify="", email=""):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(form %{"error": error, "username": username, "password": password, "verify": verify, "email": email})

    def valid_username(self, s):
        import re
        return re.match(r"^[a-zA-Z0-9_-]{3,20}$", s)

    def valid_password(self, s):
        import re
        return re.match(r"^.{3,20}$", s)

    def valid_email(self, s):
        import re
        return re.match(r"^[\S]+@[\S]+\.[\S]+$", s)

    def get(self):
        self.write_form()

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not self.valid_username(username):
          self.write_form("invalid username", escape(username), escape(password), escape(verify), escape(email))
          return

        if not self.valid_password(password):
          self.write_form("invalid password", escape(username), escape(password), escape(verify), escape(email))
          return

        if password != verify:
          self.write_form("passwords does not match", escape(username), escape(password), escape(verify), escape(email))
          return

        if email and (not self.valid_email(email)):
          self.write_form("invalid email", escape(username), escape(password), escape(verify), escape(email))
          return

        self.redirect("/welcome?username=%s" % escape(username))

class WelcomeHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Welcome: %s" % self.request.get('username'))

def main():
    application = webapp.WSGIApplication([('/', SignupHandler), ('/welcome', WelcomeHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()