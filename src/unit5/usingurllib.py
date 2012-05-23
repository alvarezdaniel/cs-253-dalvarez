#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alvarezd
#
# Created:     20/05/2012
# Copyright:   (c) alvarezd 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import urllib2

p = urllib2.urlopen("http://www.example.com")

c = p.read()

print p.headers["server"]