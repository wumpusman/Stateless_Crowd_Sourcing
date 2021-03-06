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

from manager import Manager

'''

Blueprint 

Select Top Non-Blue Print Unlocked, And Selected, Go in Numeric order [0,1,2] 
     Select First Process
          Go Through Top 2 unlocked [Or Top 1 and One Random?]
               If Like 
                    Go To Another 'Selected Process'
               Else Try Again
          If No like twice
               Create new content at that Node 
          
If No More in Selected, 
     Select All Top level UnSelected
          
               
     



'''
import pandas

def user_list_to_db(the_session,txt_list):
     seen=set()
     elements=None
     if txt_list ==None:
          elements = pandas.read_csv(os.path.join("user_list_dir", "exceptional_and_luther"))
     else:
          elements = pandas.read_csv(txt_list)
     #'0'
     #'1'
     for j in xrange(len(elements)):
          print j
          user_name = elements.iloc[j][1]
          effective = Manager.user_good_enum if elements.iloc[j][2] else Manager.user_bad
          print user_name, effective
          if (user_name in seen) ==False:

               User1 = User(the_session)
               User1.name = user_name
               User1.alias = effective
               User1.password = ''
               the_session.add(User1)

               seen.add(user_name)


#user_list_to_db(None,None)


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
     #run_example.rewrite_continuously(the_session,"little_match_girl")
     #run_example.setup_luther(the_session)
    # run_example.setup_narrative_plot(the_session)
     examples=["I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation",
              "Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation",
              "This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice",
              "It came as a joyous daybreak to end the long night of their captivity",
              "But one hundred years later, the Negro still is not free "]

     instruct=["[Give personal context to why speaker is present]",
     "[To contextualize the remarks in a larger historical context]",
     "[To provide soaring rhetoric to motivate his listeners]",
     "[Follow up on previous claim] ",
     "[Clarify that works still needs to be done]"]
    # run_example.initial_test_criteria(the_session)
     #run_example.line_by_line_rewrite_with_flex_and_testing(the_session, None, None)
     #run_example.line_by_line_rewrite_with_flex_and_testing(the_session,instruct,examples)

    # run_example.iterative(the_session, None, None)
     #print the_session.query(Content).all()
     #run_example.generate_shirt_design(the_session)

     user_list_to_db(the_session, os.path.join("backend/user_list_dir","exceptional_and_luther"))
     run_example.initial_test_criteria(the_session)

     run_example.rewrite_continuously(the_session, os.path.join("backend","little_match_girl"))

     the_session.commit()
     the_session.close()
else:

     conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test")

     meta.drop_all(bind=conn)  # clear everything
     Base.metadata.create_all(conn)
     #
     #
     #run_example.initial_test_criteria(session)

     #run_example.line_by_line_rewrite_with_flex_and_testing()
     #run_example.initial_test_criteria(session)
     #run_example.line_by_line_rewrite_with_flex_and_testing(session,None,None)

     user_list_to_db(session,None)
     run_example.initial_test_criteria(session)

     run_example.rewrite_continuously(session,"little_match_girl")
     #run_example.setup_business_advice(session)
     #run_example.setup_remapped_linear_abstract(session,"rec_template_1")
     #run_example.test_flex(session )
     #run_example.setup_general_summary(session,"sedaris_2")
     #run_example.setup_example(session)
     #run_example.setup_sedaris_high_level(session)
     #run_example.setup_sedaris(session)
     #run_example.iterative(session, None, None)
     #run_example.date_plan(session)
     session.commit()
     #run_example.setup_luther(session)
     #run_example.setup_luther(session)

     #run_example.setup_summary(session)
     session.commit()
     print session.query(Content).all()