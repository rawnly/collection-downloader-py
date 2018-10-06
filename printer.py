from __future__ import print_function

import time
import sys

items = range(10)

def printOverLast (string):
    sys.stdout.write('\r' + "%s" % string)
    sys.stdout.flush()

for item in list(items):
    time.sleep(0.2)
    printOverLast("Item {0}".format(item))
    
