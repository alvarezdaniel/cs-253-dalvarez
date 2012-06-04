from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os
import cgi
import re
import random
import hashlib
import hmac
from string import letters

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')

#def render_str(template_name, **params):
    #return template.render(template_dir + '\\' + template_name, params)
    #return repr(template_dir) + '\\' + template_name

def escape(s):
    return cgi.escape(s, quote = True)

secret = 'dalvarez'

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class WikiHandler(webapp.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template_name, **params):
        params['user'] = self.user
        #return render_str(template, **params)
        path = os.path.join(os.path.dirname(__file__), template_name)
        return template.render(path, params)

    def render(self, template_name, **kw):
        self.write(self.render_str(template_name, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class MainPage(WikiHandler):
    def get(self):
        self.write('Hello, Udacity!')

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.TextProperty(required = True)
    email = db.StringProperty()
    createdat = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
            name = name,
            pw_hash = pw_hash,
            email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

def pages_key(group = 'default'):
    return db.Key.from_path('pages', group)

class Page(db.Model):
    name = db.StringProperty(required = True)
    content = db.StringProperty(required = True, multiline=True)
    createdat = db.DateTimeProperty(auto_now_add = True)
    #createdby = db.StringProperty(required = True)
    #modifiedat = db.DateTimeProperty(auto_now = True)
    #modifiedby = db.StringProperty(required = False)

    @classmethod
    def by_id(cls, uid):
        return Page.get_by_id(uid, parent = pages_key())

    @classmethod
    def by_name(cls, name):
        u = Page.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, content):
        return Page(parent = pages_key(),
            name = name,
            content = content)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def unique_username(username):
    return User.by_name(username) == None

class Signup(WikiHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
            email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')

class Login(WikiHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(WikiHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')

class EditPage(WikiHandler):
    def get(self, name = ''):
        if True: #self.user:
            p = Page.by_name(name)
            if p:
                self.render('editpage.html', name=name, content=p.content)
            else:
                self.render('editpage.html', name=name)
        else:
            self.redirect("/login")

    def post(self, name=''):
        #if not self.user:
        #    self.redirect('/')

        #name = self.request.get('name')
        content = self.request.get('content')

        p = Page.by_name(name)
        if p:
            #p.content = 'XXX'
            #p.put()
            db.delete(p.key())

        p = Page.register(name, content)
        p.put()

        self.redirect(name)

class ViewPage(WikiHandler):
    def get(self, name = ''):

        p = Page.by_name(name)
        if p:
            self.render('viewpage.html', name=p.name, content=p.content)
        else:
            if name == '/':
                p = Page.register(name=name, content='Hello wiki!')
                p.put()
                self.redirect(name)
            else:
                self.redirect('/_edit%s' % name)

def main():
    PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
    app = webapp.WSGIApplication([('/signup', Register),
                                  ('/login', Login),
                                  ('/logout', Logout),
                                  ('/_edit' + PAGE_RE, EditPage),
                                  (PAGE_RE, ViewPage),
                                 ],
                               debug=True)

    util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
