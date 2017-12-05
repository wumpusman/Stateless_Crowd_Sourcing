import os
import urlparse
print os.environ.get('DATABASE_URL')
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.orm import backref
from sqlalchemy import func
import pandas as pd
Base=declarative_base()
if type(os.environ.get('DATABASE_URL')) != type(None):
     url = os.environ.get('DATABASE_URL')#urlparse.urlparse(os.environ.get('DATABASE_URL'))

     print "great"
     print "URL FOUND"
     con = sqlalchemy.create_engine(url, client_encoding='utf8')

     # We then bind the connection to MetaData()
     meta = sqlalchemy.MetaData(bind=con, reflect=True)

     Session = sessionmaker(bind=con)

     the_session=Session()
     print "GREAT"