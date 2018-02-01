import os
import urlparse
print os.environ.get('DATABASE_URL')
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from db_connection2 import *
from sqlalchemy.orm import backref
from sqlalchemy import func
import pandas as pd
import run_example
#pg_restore -h localhost -U username -W -F t -d new_database_name database_dump_file.tar
if type(os.environ.get('DATABASE_URL')) != type(None):
     url = os.environ.get('DATABASE_URL')#urlparse.urlparse(os.environ.get('DATABASE_URL'))
          #s

     con = sqlalchemy.create_engine(url, client_encoding='utf8')

     # We then bind the connection to MetaData()
     meta = sqlalchemy.MetaData(bind=con, reflect=True)

     Session = sessionmaker(bind=con)

     the_session=Session()

     meta.drop_all(bind=con)  # clear everything
     Base.metadata.create_all(con)
     the_session.commit()


     ''' 
     text_body="I read a lot about cognition, math, brains, and the social sciences, because I wonder a lot about how people work. " \
               "For now I'm focusing on my job in linguistics and software, " \
               "but I'd like to make some advances in AI. I'm fortunate to have many friends who live nearby, and I'm enjoying spending time with them."

     run_example.question_answer_profile_generation(the_session,text_body=text_body,assign_user=True)



     text_body= "I enjoy long walks, and I meditate to reduce anxiety, which constantly bubbles up to the surface if I stay still for too long. " \
                "I identify as a feminist, a Unitarian Universalist, a pragmatist, an effective altruist, and a left libertarian."

     run_example.question_answer_profile_generation(the_session,text_body=text_body, assign_user=False)



     text_body="I'm an introvert who enjoys reading and going for long, contemplative walks. I enjoy playing dungeons and dragons and videogaming, " \
               "but I also enjoy cooking and going to the gym. I'm looking for a smart, curious woman who enjoys conversation and science."
     run_example.question_answer_profile_generation(the_session, text_body=text_body, assign_user=False)
     '''
     run_example.rewrite_continuously(the_session,"little_match_girl")
     #run_example.setup_luther(the_session)

     the_session.commit()
     print the_session.query(Content).all()

else:
     conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test")

     meta.drop_all(bind=conn)  # clear everything
     Base.metadata.create_all(conn)
     #
     #

     session.commit()
     run_example.rewrite_continuously(session,"little_match_girl")
     run_example.setup_luther(session)
     #run_example.setup_luther(session)

     #run_example.setup_summary(session)
     session.commit()
     print session.query(Content).all()