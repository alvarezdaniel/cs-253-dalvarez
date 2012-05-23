import random
import string
import hashlib

def make_salt():
    random.seed(0)
    return ''.join(random.choice(string.letters) for x in xrange(5))

# Implement the function valid_pw() that returns True if a user's password
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]

    #print h
    #h2 = make_pw_hash(name, pw, salt)
    #print h2

    return h == make_pw_hash(name, pw, salt)

h = make_pw_hash('spez', 'hunter2')
#print h
print valid_pw('spez', 'hunter2', h)

