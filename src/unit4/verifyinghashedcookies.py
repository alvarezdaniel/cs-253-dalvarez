import hashlib

def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    return "%s,%s" % (s, hash_str(s))

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(h):
    a = h.split(",")
    hash2 = hash_str(a[0])
    if hash2 == a[1]:
        return a[0]
    
#cookie = make_secure_val("hola")
#print cookie
#s = check_secure_val(cookie)
#print s
#cookie = "%s0" % cookie
#s = check_secure_val(cookie)
#print s


                         



