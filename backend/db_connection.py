import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ARRAY, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum
from sqlalchemy.orm import backref
def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    Session = sessionmaker(bind=con)
    return con, meta,Session()


Base =declarative_base()

class Users (Base):
    __tablename__ = 'users'
    name=Column('name', String, primary_key=True)
    alias=Column('alias',String) #just an alternate to their name
    password=Column('password', String)
    current_content_id=Column('current_content_id', String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    #
    associated_content=relationship('Content',backref='users',cascade="all,delete")
    def __repr__(self):
        return "<Table User {}>".format(self.name)

    def __init__(self,name):
        self.name=name

'''
class Project(Base):
    __tablename__ = 'project'
    name=Column('name', String, primary_key=True)
    content_types_allowed=Column('content_types', ARRAY(String))
    notes=Column('Notes', String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return "<Table Project {}>".format(self.name)

'''

class Process_Object(Base):
    __tablename__='process_object'
    id=Column('id',Integer,primary_key=True)
    content_id=Column(Integer, ForeignKey('content.id'))
    content = relationship('Content',back_populates="process_object") #reference content that i'm trying to handle

    #user_responses=relationship('Content',backref='process_object')
    #map content
    '''
    Process_Object_ID
    Type_ID

    Content_ID
    Content_To_Examine

    List_User_Responses(Unassigned) - Associated
    Content
    List_Associated_Sub_Processes

    GetResult()
    '''

class Content(Base):
    __tablename__ = 'content'
    id=Column('id', Integer, primary_key=True)
    content_type=Column('content_type', String) #the content to be parsed
    comments=Column('comments', String) # any notes
    results=Column('results',String) #the actual content the user entered
    rating=Column('rating',String) #how do they rate the content of results, unless type is 'rating'

    user_id=Column(String,ForeignKey('users.name')) #What user created this content
    project_id=Column(String, ForeignKey('project.name')) #what project is this affliated iwth
    parent_id=Column(Integer, ForeignKey('content.id')) #content this is basing itself on

    is_completed=Column('is_completed', Boolean, default=False)  # has the user finished this content - or this iteration
    is_locked=Column('is_locked', Boolean,default=False)  # can it be modified or edited
    is_chosen=Column('is_chosen', Boolean,default=False) # has it been deemed 'worthy' to be used again

    created_date = Column(DateTime, default=datetime.datetime.utcnow) #base this function to evaluate at run time

    parent_content=relationship('Content',remote_side=[id]) #so i can reference the content that I came from, it lets me loop through iteratively

    user_create=relationship('Users',backref='content',cascade="all,delete")


    associated_processes=relationship("Process_Object",back_populates="content") #children = relationship("Child", back_populates="parent")

    def __init__(self):

        pass

'''
class Task_Instruction(Base):
    __tablename__='task_instructions'
    name=Column('name',String, primary_key=True)
    task_type=('type',String) #what kind of content am i helping with
    explanation=('explanation',String)
    additional_info=('supplemental',String) #is there any info that i need to supplement
'''



class Content_Types(Enum):
    Rate="Rate"
    Summarize="Summarize"
    Rewrite="Rewrite"
    Merge="Merge"
    Sugeest="Suggest"


if __name__ == '__main__':
    conn,meta,session=connect("postgres","1234",db="Task_Crowd_Source") #user='postgres', password='1234'
    Base.metadata.create_all(conn)


    user1=Users("STALIN")
    user1.password="324"
    cont1=Content()
    cont1.id=11
    cont1.results="I am stalin"
    cont1.user_id=user1.name

    cont2=Content()

    cont2.results="modification of stalin"
    cont2.parent_id=cont1.id
    cont2.user_id=user1.name

    d=Process_Object()
    d.content_id=cont2.id
    d.content=cont2

    session.add(user1)
    session.add(cont1)
    session.add(cont2)
    session.add(d)


    print "OK "
    user1.password="gijoe"


    result=session.query(Process_Object)

    for j in result:

        j.content.results
    #
    '''

    Process
        Logic()
        List ->User_Responses
        List->Child_Process

    Process_Rewrite_Simple
        Logic()
        Predecessor

        Content_ID
        Content_To_Examine

        Finished=False

        IsFinished():
            If Have At Least 1 Score > 1

        List->User_Response
        List->Rate_Content_Process(User_Response,Parent_Process)
        GetResults(User_Response, Associated_Process)



    ProcessObject
        Process_Object_ID
        Type_ID

        Content_ID
        Content_To_Examine


        List_User_Responses(Unassigned) - Associated Content
        List_Associated_Sub_Processes

        GetResult()




    Process_Suggestions_Simple()
        Logic()
        Previous_Step_Process


        Content_To_Examine

        IsFinished():
            If Have at least 1 Score > 1

        List->User_Response
        List->Rate_Content_Process(User_Response,Parent_Process)
        GetResults(





    Rate_Rewrite_Process(Response_To_Rewrite,Process_Come_From)
        Logic()
        Content_To_Examine=Response_To_Rewrite

        List->User_Response

        GetResults(User_Response)
            Is_Finished()
                return CalculateScore()

        Is_Finished()
            If_User_Responses Completed > 3:
                Return True

        CalculateScore()


    User = Table ('users', meta,
                  Column('name',String,primary_key=True),
                  Column('password',String),
                  Column('current_content_id',String)
                  )

    Project = Table('project', meta,
                 Column('name', String, primary_key=True),
                 Column('Content_Types', ARRAY(String)),
                 Column('Notes',String)
                 )

    Content = Table('content', meta,
                 Column('content_id', String, primary_key=True),
                 Column('Content_Type', String),
                 Column('comments', String),
                 Column('parent_content_id',String),
                 Column('is_completed',Boolean), #has the user finished this content - or this iteration
                 Column('is_locked',Boolean), #can it be modified or edited
                 Column('is_chosen',Boolean), #has it been deemed 'worth to be used again
                 )
    '''