#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alvarezd
#
# Created:     21/05/2012
# Copyright:   (c) alvarezd 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

d = {"blah":["one", 2, 'th"r"ee']}

import json

s = json.dumps(d)
print s