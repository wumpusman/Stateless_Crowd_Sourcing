import datetime
current_time_minus_X = datetime.timedelta(minutes=4)
current_time_minus_X = (datetime.datetime.now() - current_time_minus_X)
print current_time_minus_X.now()
print datetime.datetime.now()


import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ARRAY, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis

    if type(os.environ.get('DATABASE_URL')) != type(None):
        url = os.environ.get('DATABASE_URL')  # urlparse.urlparse(os.environ.get('DATABASE_URL'))


        con = sqlalchemy.create_engine(url, client_encoding='utf8')

        # We then bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=con, reflect=True)

        Session = sessionmaker(bind=con)

        the_session = Session()
        return con,meta,the_session
    else:
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)

        # The return value of create_engine() is our connection object
        con = sqlalchemy.create_engine(url, client_encoding='utf8')

        # We then bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=con, reflect=True)

        Session = sessionmaker(bind=con)




        return con, meta,Session()