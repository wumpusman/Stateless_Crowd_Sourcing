import os
import urlparse
print os.environ.get('DATABASE_URL')
if type(os.environ.get('DATABASE_URL')) != type(None):
     url = urlparse.urlparse(os.environ.get('DATABASE_URL'))

     print "great"
     print "URL FOUND"