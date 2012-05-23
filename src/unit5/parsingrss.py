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
from xml.dom import minidom

contents = urllib2.urlopen("http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml").read()

d = minidom.parseString(contents)

items = d.getElementsByTagName("item")
print len(items)