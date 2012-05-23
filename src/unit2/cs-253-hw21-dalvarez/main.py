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
<form method="post" action="/rot13">
  <input type="text" name="text" >
  <input type="submit">
</form>
"""

def escape_html(s):
  return cgi.escape(s, quote = True)

def rot13(s):
  return s.encode('rot13')

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(form)

class Rot13Handler(webapp.RequestHandler):
    #def get(self):
    #    self.response.out.write('get')

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'

        text = self.request.get('text')
        rot13_text = rot13(text);

        self.response.out.write(escape_html(rot13_text));


def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/rot13', Rot13Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
