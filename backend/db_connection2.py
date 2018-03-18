import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ARRAY, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import backref
from sqlalchemy import func
import pandas as pd
import os

Base=declarative_base()

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




class User (Base):
    __tablename__ = 'user'
    name=Column('name', String, primary_key=True)
    alias=Column('alias',String) #just an alternate to their name
    password=Column('password', String)

    current_content_id=Column('current_content_id',ForeignKey("content.id"))
    current_content=relationship("Content",foreign_keys=[current_content_id],uselist=False)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    associated_content =relationship("Content", backref="associated_user",foreign_keys="Content.user_id")



    def get_current_content_in_progress(self,session):

       query=self.get_all_user_assigned_content(session)
       query=query.filter(Content.is_completed==False)

       alt=Process_Object.get_processes_that_are_ready(session)
       alt=alt.filter(Process_Object.is_locked==False).subquery()
       query=query.filter(Content.origin_process_id==alt.c.id ).all()

       '''
       if len(query)>1:
           raise Exception("Get Current Content Have multiple incomplete content associated with this elemtn ")
       elif len(query)==0:
           return None
       else:
           return query[0]
        '''
       print "content length"
       print len(query)
       if len(query)==0: return None
       if len(query) >1:
           query.sort(key=lambda x: x.id, reverse=True)
           print query[0]
           print query[1]
           #raise Exception("Multiple content assigned  to this user, this forces an error since this should not be "
            #                             "the normal case. I need to refactor so specific processes are designated to particular users")
       return query[0]
    def get_all_user_assigned_content(self,session):
        return session.query(Content).filter(Content.user_id  == self.name)

    def get_all_processes_where_user_was_uninvolved(self,session):

        first=self.get_all_user_assigned_content(session).subquery()
        second=session.query(Process_Object.id).filter(first.c.origin_process_id==Process_Object.id).all() #get all processes associated iwth this

        if len(second) ==0: #If has no associated objects
            return session.query(Process_Object)

        third = session.query(Process_Object).filter(~Process_Object.id.in_(second)) #otherwise reutrn everything

        return third

    def get_all_unassigned_and_available_content_where_user_was_uninvolved(self,session):
        from sqlalchemy import and_ as and_

        legal_processes=Process_Object.get_processes_that_are_ready(session).subquery("legal_processes") # I REALLY NEED TO MODIFY THIS

        #print Process_Object.get_processes_that_are_ready(session).all()
        print "ARE YOU SUTTER CANE"
        uninvolved_processes=self.get_all_processes_where_user_was_uninvolved(session).subquery("uninvolved_processes")

        self.get_all_processes_where_user_was_uninvolved(session).all()

       # print self.get_all_processes_where_user_was_uninvolved(session).all()
        import time
        start=time.time()
        uncompleted_and_unlocked_processes= session.query(Process_Object).\
            filter(Process_Object.id==uninvolved_processes.c.id).\
            filter(Process_Object.id==legal_processes.c.id).\
            filter(Process_Object.is_locked==False).\
            filter(Process_Object.is_completed==False)

        #session.query(Process_Object).filter(Process_Object.id==uninvolved_processes.c.id).all()
        session.query(Process_Object).filter(Process_Object.id == legal_processes.c.id).all()
        #uncompleted_and_unlocked_processes.all()
        print time.time()-start
        start=time.time()
        uncompleted_and_unlocked_processes = session.query(Process_Object).filter(and_(

            (Process_Object.id == uninvolved_processes.c.id),
            (Process_Object.id == legal_processes.c.id),
            (Process_Object.is_locked == False),
            (Process_Object.is_completed == False)))

        print "AND THIS?"
        #uncompleted_and_unlocked_processes.all()
        print time.time()-start
        available_content_to_edit=session.query(Content).filter(Content.origin_process_id==uncompleted_and_unlocked_processes.subquery().c.id).filter((Content.user_id==None) & (Content.is_completed==False) & (Content.is_locked==False))
        print "I AM SUTTER CANE"
        return available_content_to_edit

    def get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self,session):

        available_content_to_edit=self.get_all_unassigned_and_available_content_where_user_was_uninvolved(session )

        get_cont = session.query(Content).filter(self.name == Content.user_id).subquery()
        get_tasks = session.query(Task_Parameters).filter(get_cont.c.id == Task_Parameters.result_id).subquery()
        get_rate_processes = session.query(Process_Rate.id).filter(
            get_tasks.c.id == Process_Rate.task_parameters_id).all()

        print "content where user is uninvolved and is fine???"
        if len(get_rate_processes) > 0:
            print "INSIDE HERE?"
            available_content_to_edit_minus_where_user_created_content_that_is_being_rated = \
                session.query(Content).filter(available_content_to_edit.subquery().c.id == Content.id).filter(
                    ~(Content.origin_process_id.in_(get_rate_processes)))
            return available_content_to_edit_minus_where_user_created_content_that_is_being_rated
        print "what abotu his point"
        return available_content_to_edit
    def __repr__(self):
        return "<Table User {}>".format(self.name)

    def __init__(self,name):
        self.name=name


class Project(Base):
    __tablename__ = 'project'
    id = Column('id', String, primary_key=True) #a conceptual project

    root_process_id=Column('root_process_id',Integer,ForeignKey('process_object.id'))

    root_process=relationship("Process_Object",foreign_keys=[root_process_id]) #the source of all


    #has all processes connected to it





class Process_Object(Base):
    __tablename__='process_object'


    id=Column('id',Integer,primary_key=True)
    parent_id= Column("PARENTID", Integer, ForeignKey('process_object.id'))
    parent_process=relationship("Process_Object",remote_side=[id],uselist=False)


    task_parameters_id = Column('task_parameters_id',Integer, ForeignKey('task_parameters.id'))

    minimum_amount_of_content_being_requested = Column("minimum_amount_of_content_being_requested", Integer, default=3)

    task_parameters_obj= relationship('Task_Parameters',foreign_keys=[task_parameters_id],back_populates='parent_process',uselist=False)

    is_locked=Column('is_locked', Boolean, default=False) #can this be used/is it accesible
    is_completed=Column('is_completed', Boolean, default=False) #can this be used/is it accesible
    is_using_ml=Column("is_using_ml",Boolean,default=False)


    created_date = Column(DateTime, default=datetime.datetime.utcnow)  # base this function to evaluate at run time
    completed_date = Column(DateTime)


    sub_process = relationship("Process_Object",foreign_keys=[parent_id]) #so i can have arbitrary sub processes running on elements being produced with this

    #implicitely also has self.children - see Content
    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    #am i going to use some sort of ml model to rate ocntent or weight rating
    def get_rating_ml_model_result(self,path,data_to_evaluate):
        pass


    #is the task found stuff
    def is_complete(self,session):
       final_results= self.get_final_results_complete(session).all()
       if len(final_results) == len(self.get_final_results()):
           return True
       return False

    def get_expected_completion_read_ratio(self,content_obj):
        print content_obj
        print "this is whose date it being evaluated"
        completion_time = content_obj.get_completion_time()
        read_time = self.task_parameters_obj.estimate_read_time()

        ratio =float ( completion_time) / float(read_time)
        return ratio

    def lock_process(self):
        self.is_locked=True
        if len(self.sub_process)>0:
            for sp in self.sub_process:
                sp.is_locked=True

    def assign_user(self,user_obj):
        #Assign this process and all sub problems to a specific user
        associated_content=self.get_content_produced_by_this_process()
        for i in associated_content:
            if i.user_id !=None:
                raise Exception("User already assigned!")
            i.associated_user = user_obj
            i.user_id=user_obj.name

        for i in self.sub_process:
            for j in i.get_content_produced_by_this_process():
                if j.user_id != None:
                    raise Exception("User already assigned!")
                j.associated_user = user_obj
                j.user_id=user_obj.name


    def __init__(self,body_of_task=None,prompt=None,suggestion=None,context=None, displayed_result=None, expected_results=1, content_to_be_requested=3, subprocess_tuple=None):
        #displayed result is only for rating tasks, where user is reviewing a result

        self.ml_model=None #
        self.is_using_ml=False
        self.is_locked=False
        self.is_completed=False

        self.task_parameters_obj=Task_Parameters(body_of_task=body_of_task,prompt=prompt,result=displayed_result,suggestion=suggestion,context=context,parent_process=self )
        self.minimum_amount_of_content_being_requested=content_to_be_requested

        for i in xrange(expected_results):
            self.get_final_results().append(Content_Result())  # BY default there should be at least one




        for i in xrange(content_to_be_requested):
            user_cont=Content()
            self.get_content_produced_by_this_process().append(user_cont)
            if type(subprocess_tuple)!=type(None): #if there is a subprocess associated iwth this taask

                pr_type=subprocess_tuple[0]
                if subprocess_tuple[1]['content_to_be_requested']==0: continue #If nothing is expected ot be reviewed than don't review the content


                a_sub_process=pr_type(body_of_task=body_of_task,displayed_result=user_cont,**subprocess_tuple[1])
                self.sub_process.append(a_sub_process)

    @staticmethod
    def get_processes_that_are_ready(session):
        #This will return processes regardless of type
        all_available_tasks=Task_Parameters.get_tasks_that_are_ready(session).subquery()




        result=session.query(Process_Object).filter((Process_Object.task_parameters_id==all_available_tasks.c.id)
                                                ).filter(Process_Object.is_locked==False)

        return result


    def select_data_for_analysis(self,session): #this is the data, that is gonna be used to generate results for this system

        if len(self.sub_process) > 0: #If I have any subprocesses, assume this thing requires subprocesses
            result=self._select_data_that_has_subprocesses(session)


            result=[(i.process_that_selected_this_content.task_parameters_obj.result,i) for i in result ] #the content and the results tha
            return result

        else:
            result=self._select_data(session)
            result=[(i,i) for i in result if i.is_locked==False ]
            return result


    def _select_data_that_has_subprocesses(self,session): #RESLUT IN TASK PARAMETER IS always assumed ot be the link to previous element
        get_self = session.query(Process_Object).filter(Process_Object.id == self.id).subquery("get_self")
        get_content_stemming_from_this_process = session.query(Content).filter(
            Content.origin_process_id == get_self.c.id).filter((Content.is_completed == True) & (Content.is_locked==False)).subquery(
            "get_content_stemming_from_this_process")



        tasks_associated_with_this_content = session.query(Task_Parameters).filter(Task_Parameters.result_id == get_content_stemming_from_this_process.c.id).\
            subquery("tasks_associated_with_this_content")




        processes_associated_with_this_task = session.query(Process_Object).filter(Process_Object.task_parameters_id == tasks_associated_with_this_content.c.id).subquery(
            "processes_associated_with_this_task")  # suprocesses

        relevant_results = session.query(Content).filter(
            Content.process_that_selected_this_content_id == processes_associated_with_this_task.c.id).filter(Content.is_completed==True).all()  # process_that_selected_this_content_id

        return relevant_results



    def _select_data(self,session):
         get_self = session.query(Process_Object).filter(Process_Object.id == self.id).subquery("get_self")
         return session.query(Content).filter(
            Content.origin_process_id == get_self.c.id).filter(Content.is_completed==True).all()


    def prepare_view(self):
       task_view=self.task_parameters_obj.prepare_view()
       task_view["Type"]=str(type(self))

       instructions=self.prepare_instructions()

       task_view["instructions"]=instructions
       return task_view



    def prepare_instructions(self):
        prepped_instructions={}
        explanation=" You will be shown a small amount of text and be asked to modify it the best of your ability based on a prompt. " \
                    "Make changes as best you can, but do not overthink it. This is only meant to take a few minutes. You may be asked to rewrite, modify or summarize " \
                    "text. You will also be potentially provided some contextual information as well as suggestions to help aid you.  "
        exampe_rewrite="<p><u>More suspenseful</u>: The man walked to the store' <b>-></b> 'The man frantically hurried to the shop'</p>"
        exampe_rewrite1="<p><u>Write as though the story was about a boy </u> : The man entered the bar' <b>-></b> 'The boy entered the game shop'</p>"
        example_summary="'<p><u>Summarize </u>: The man walked to the store to buy some ice cream' <b>-></b> 'A man got some ice cream'</p>"
        example_suggestion="<p><u>Suggest ways you might rewrite the text to talk about medical issues:</u> 'Boy can teach you to bottle charisma, brew glory, even put a stopper in death <b>-></b> Maybe talk about actual conditions, like bottle ingestion, or brew a cure for diabetes  </p>"


        prepped_instructions={"Explanation":explanation,"Examples":[exampe_rewrite,exampe_rewrite1,example_summary,example_suggestion]}
        return prepped_instructions

    def get_final_results(self):
        return self.final_results

    def get_final_results_incomplete(self,session):

        return session.query(Content_Result).filter((Content_Result.process_that_selected_this_content_id==self.id) & (Content_Result.is_completed==False))

    def get_final_results_complete(self, session):

        return session.query(Content_Result).filter((Content_Result.process_that_selected_this_content_id == self.id) & (Content_Result.is_completed == True))


    def get_content_produced_by_this_process_that_is_complete(self,session):



        return session.query(Content).filter(
            (Content.origin_process_id == self.id) & (Content.is_completed == True))

    def get_content_produced_by_this_process(self):
        return self.user_content_being_generated_from_this_process


    def print_out(self):
        print len(self.user_content_being_generated_from_this_process)





'''
Define 'Project Flow'
    Process_Rewrite       -> Process_Rewrite    -> Process_Summary                    Process_Suggest -> Merge_Step
            Process_Rate            Process_Rate       returns Content_To_BE_Written, Suggestions


User Signs In,  Assign Content
On User Return, if has content is incomplete or null:
    Request New Content

On User Submit Content
    Assign as finished, assign result, assign parent result

'''

class Task_Parameters(Base): #contains all the information pertinent to what a user can manipulate on the screen except ratings - this is updated at the end of a process, this can be passed from a process
    __tablename__ = 'task_parameters'
    id =  Column('id', Integer, primary_key=True) #a conceptual project

    prompt_id=Column('prompt_id',Integer, ForeignKey('content.id'))
    suggestion_id=Column('suggestion_id',Integer, ForeignKey('content.id'))
    context_id=Column('context_id',Integer, ForeignKey('content.id'))
    body_of_task_id=Column('body_of_task_id',Integer, ForeignKey('content.id'))
    result_id=Column('result_id',Integer,ForeignKey("content.id"))

    prompt=relationship('Content',foreign_keys=[prompt_id])
    suggestion = relationship('Content', foreign_keys=[suggestion_id])
    context = relationship('Content', foreign_keys=[context_id])
    body_of_task=relationship('Content', foreign_keys=[body_of_task_id])
    result=relationship('Content',foreign_keys=[result_id]) #The result from a different task for rating purposes

    parent_process=relationship("Process_Object",back_populates="task_parameters_obj",uselist=False) #who am i associated iwth, what process created me

    def is_task_ready(self):
        is_ready=True

        components=[self.prompt,self.result,self.context,self.body_of_task,self.suggestion]
        for component in components:
            if component.is_completed==False:
                return False
        return True

    @staticmethod
    def get_tasks_that_are_ready(session):


        completed_content=session.query(Content).filter(Content.is_completed==True).subquery()


        body_of_task_query = session.query(completed_content).filter(
            (completed_content.c.id == Task_Parameters.body_of_task_id)).subquery()
        task_params_with_finished_X = session.query(Task_Parameters).filter(
            body_of_task_query.c.id == Task_Parameters.body_of_task_id).subquery()

        suggestion_query = session.query(completed_content).filter(
            (completed_content.c.id == Task_Parameters.suggestion_id)).subquery()
        task_params_with_finished_Y = session.query(Task_Parameters).filter(
            suggestion_query.c.id == Task_Parameters.suggestion_id).subquery()

        context_query = session.query(completed_content).filter(
            (completed_content.c.id == Task_Parameters.context_id)).subquery()
        task_params_with_finished_Z = session.query(Task_Parameters).filter(
            context_query.c.id == Task_Parameters.context_id).subquery()


        prompt_query = session.query(completed_content).filter(
            (completed_content.c.id == Task_Parameters.prompt_id)).subquery()
        task_params_with_finished_ZZ = session.query(Task_Parameters).filter(
            prompt_query.c.id == Task_Parameters.prompt_id).subquery()

        result_query = session.query(completed_content).filter(
            (completed_content.c.id == Task_Parameters.result_id)).subquery()
        task_params_with_finished_ZZZ = session.query(Task_Parameters).filter(
            result_query.c.id == Task_Parameters.result_id).subquery()


        ok=session.query(task_params_with_finished_X).join(task_params_with_finished_Y,task_params_with_finished_X.c.id==task_params_with_finished_Y.c.id).distinct().subquery()
        ok=session.query(ok).join(task_params_with_finished_Z,ok.c.id==task_params_with_finished_Z.c.id).distinct().subquery()
        ok = session.query(ok).join(task_params_with_finished_ZZ,
                                    ok.c.id == task_params_with_finished_ZZ.c.id).distinct().subquery()
        ok = session.query(ok).join(task_params_with_finished_ZZZ,
                                    ok.c.id == task_params_with_finished_ZZZ.c.id).distinct().subquery()


        tasks_that_are_ready = session.query(ok)
        #task_query = session.query(task_params_with_finished_X).filter(Task_Parameters.id==task_params_with_finished_X.c.id)

        return tasks_that_are_ready #




    def __init__(self,body_of_task,prompt=None,suggestion=None,context=None,result=None,parent_process=None):
        #If They are empty make a wrapper, this should never bthe case in actuality
        if prompt ==None:
            prompt=Content()
            prompt.is_completed=True
        if suggestion==None:
            suggestion=Content()
            suggestion.is_completed=True
        if context==None:
            context=Content()
            context.is_completed=True
        if result==None:
            result=Content()
            result.is_completed=True
        if body_of_task == None:
            body_of_task = Content()
            body_of_task.is_completed = True

        self.body_of_task=body_of_task
        self.prompt=prompt
        self.suggestion=suggestion
        self.context=context
        self.parent_process=parent_process
        self.result=result

    def estimate_read_time(self):

            total_text = ""
            total_text += " " + self.body_of_task.results
            total_text += " " + self.prompt.results
            total_text += " " + self.result.results
            total_text += " " + self.suggestion.results
            total_text += " " + self.context.results
            words = len(total_text.split(" "))
            time = words / 5.5

            return time


    def prepare_view(self):
        print "THIS VIEW"
        print self.parent_process.id
        print self.body_of_task.id
        print self.body_of_task.results
        front_end_view={
            "Prompt":self.prompt.results,
            "Suggestion":self.suggestion.results,
            "Context":self.context.results,
            "Body_Of_Task":self.body_of_task.results,
            "Previous_Result":self.result.results
        }
        return front_end_view


class Process_Rate(Process_Object):
    __mapper_args__ = {'polymorphic_identity': 'process_rate'}



    def _get_content_completed_counts(self, session):
        #All results stemming from this data, assumes numerical, and was not empty
        current_content=session.query(Content).filter((self.id==Content.origin_process_id) & (Content.is_completed==True) & (Content.results!="")).subquery()


        result= session.query(current_content).all()

        alt=pd.DataFrame(result)

        return alt["results"].value_counts()



    def _can_assign_result(self,session):
        #can have more complex rules account for more variance and such
        count_score=None

        try:
            count_score=self._get_content_completed_counts(session)
        except:
            return False

        if count_score.sum() < self.minimum_amount_of_content_being_requested: #count how many people created content
            return False
        return True

    def _calculate_score(self,session):
        score = 0

        results = self._get_content_completed_counts(session)
        for j in results.index:
            occurrences = results[j]
            amount = j
            if j=="Issue":
                amount="-2"
            if j == 'issue':
                amount = "-2"

            score += (float(amount) * occurrences)

        total_score = score / results.sum()

        return total_score
    #Basic rule for assigning a score, suepr naive, but i don't care atm, return one result
    def assign_result(self,session):
        if self._can_assign_result(session):

            score=self._calculate_score(session)

            empty_results=self.get_final_results_incomplete(session).all()

            assume_first_one=empty_results[0]
            assume_first_one.results=str(score)
            assume_first_one.is_completed=True
            assume_first_one.is_locked=True
            assume_first_one.completed_date=datetime.datetime.now()

    def prepare_view(self):
        prep_view=super(Process_Rate, self).prepare_view()
        prep_view["Type"] = "Rate" #Process is going to be doing rating
        return prep_view

    def prepare_instructions(self):
        prepped_instructions = {}
        explanation = "You will be shown text and asked to compare or evaluate it. You must then rate it from a 1 to a 5 (5 being the highest) based on the requirements of a prompt. If you notice an issue or problem" \
                      " delineate it by clicking issue. Try to account for the prompt as well as the overall quality of the text to be evaluated"

        exampe_rate1 = "<p><u>Rate how well the later text makes the former more suspenseful</u>: The man walked to the store' <b>vs</b> 'The man frantically hurried to the shop' Rating:5"
        example_summary_rate = "<p><u>Rate how well the later summarizes the former </u>: The man walked to the store to buy some ice cream' <b>vs</b>  'A man walked to a place' Rating:2"
        example_suggestion_rate = "<p><u>Rate how well the later suggestions may aid in rewriting the text to discuss medical issues</u>: 'I can teach you to bottle charisma, brew glory, even put a stopper in death <b>vs</b>  Maybe talk about actual conditions, like bottle ingestion, or brew a cure for diabetes' Rating:4 "

        prepped_instructions = {"Explanation": explanation,
                                "Examples": [exampe_rate1, example_summary_rate, example_suggestion_rate]}
        return prepped_instructions


class Process_Text_Manipulation(Process_Object): #Assumes i'm getting some rating, it's really basic selection scoring scheme
    __mapper_args__ = {'polymorphic_identity': 'process_text_manipulation'}

    def initialize_user_content(self, type_of_subprocess=Process_Rate):
        super(Process_Rewrite, self).initialize_user_content(amount, type_of_subprocess)




    def _can_assign_result(self, session):

        tuples_of_results=self.select_data_for_analysis(session) #data associated with whatever I have available to make a decision

        if len(self.get_final_results())==len(self.get_final_results_complete(session).all()): return False

        if len(tuples_of_results)>=len(self.get_final_results()): #do i have minimum data to make a decision
            return True
        return False



    def assign_result(self,session):

        if self._can_assign_result(session):
            data=self.select_data_for_analysis(session)


            data.sort(key=lambda x: float(x[1].results),reverse=True) #best go first

            best_results=[]

            if len(self.sub_process)!=0: #if we have scores

                for item in data:
                    if float(item[1].results)>=3:
                        best_results.append(item[0]) #store the actual value, not the score

            else: #if we are just doing the mainstream thing of scoring elements
                best_results=[item[0] for item in data]

            for counter in xrange(len(best_results)):

                item=best_results[counter]


                available_result_slots = self.get_final_results_incomplete(session).all()  # get results that are incomplete

                if len(available_result_slots)==0: break


                chosen_result=available_result_slots[0]

                item.is_locked=True #Can't use anymore
                #We foudn a result!
                chosen_result.is_locked=True
                chosen_result.is_completed=True

                #assign the content result a value
                chosen_result.linked_content=item
                chosen_result.results=item.results

    def prepare_view(self):
        task_view=super(Process_Text_Manipulation, self).prepare_view()
        task_view["Type"] = "Rewrite"
        return task_view


class Process_Rewrite(Process_Text_Manipulation): #assume i'm gonna rate the subprocesses
    __mapper_args__ = {'polymorphic_identity': 'process_rewrite'}

    def initialize_user_content(self,type_of_subprocess=Process_Rate):
        super(Process_Rewrite, self).initialize_user_content(amount,type_of_subprocess)


    def _can_assign_result(self, session):
        if len(self.sub_process) == 0: return True #if no evalaution just assign result

        tuples_of_results=self.select_data_for_analysis(session) #data associated with whatever I have available to make a decision

        if len(self.get_final_results())==len(self.get_final_results_complete(session).all()): return True

        if len(tuples_of_results)>=len(self.get_content_produced_by_this_process()): #do i have ALL THE data to make a decision
            return True
        return False


    def get_rating_ml_model_result(self,path,data_to_evaluate):
        if data_to_evaluate[0]==data_to_evaluate[1]: return 5

        content_object=data_to_evaluate[0]
        score=float(data_to_evaluate[1].results)

        ratio=self.get_expected_completion_read_ratio(content_object)

        if ratio < 1.3:
                if score > 3:
                    score =3
                print ratio
                print score
                return score * ratio #make it slightly worse than 3

        return score

    def assign_result(self, session):

        if self._can_assign_result(session):
            data = self.select_data_for_analysis(session)

            alt=[]
            best_results = []


            for item in data:
                if  (self.is_using_ml == False): #if not using ML
                    alt.append((item[0],item[1].results))
                else: #this implicitely will handle it if no rating scheme
                    alt.append((item[0],self.get_rating_ml_model_result("",(item[0],item[1])))) #modify score based on a metric



            data=alt
            data.sort(key=lambda x: float(x[1]), reverse=True)  # best go first



            if len(self.sub_process)!=0: #if there are ways to rate the content
                for item in data:

                    print item[1]
                    if float(item[1]) > 4:
                        best_results.append(item[0])  # store the actual value, not the score
                    elif len(data)>=len(self.get_content_produced_by_this_process()): #if we have completely filled out results
                        best_results.append(item[0])

            else:  # if we are just doing the mainstream thing of taking whatever was passed to us
                best_results = [item[0] for item in data]


            for counter in xrange(len(best_results)):

                item = best_results[counter]

                available_result_slots = self.get_final_results_incomplete(
                    session).all()  # get results that are incomplete

                if len(available_result_slots) == 0: break

                chosen_result = available_result_slots[0]

                item.is_locked = True  # Can't use anymore
                # We foudn a result!
                chosen_result.is_locked = True
                chosen_result.is_completed = True

                # assign the content result a value
                chosen_result.linked_content = item
                chosen_result.results = item.results


class Process_Modify_Results_And_View(Process_Rewrite): #assume i'm gonna rate the subprocesses
    __mapper_args__ = {'polymorphic_identity': 'process_modify_results'}


    def assign_result(self, session):
        super(Process_Modify_Results_And_View, self).assign_result(session)
        if len(self.get_final_results()) == len(self.get_final_results_complete(session).all()):
            actually_done=self.get_final_results_complete(session)
            for content in actually_done:
                content.results=self.task_parameters_obj.body_of_task.results+ " " +content.results
    '''
       Context Instruction 
       View
        Body Of Task View = Body Of Task + Context
        Context = ""
       Result:
        
       Final Result = Body Of Task + Final Result 
       
    '''
    def prepare_view(self):
        task_view = super(Process_Modify_Results_And_View, self).prepare_view()

        task_view["Body_Of_Task"]=task_view["Body_Of_Task"] + task_view["Context"]
        task_view["Context"]=""

        return task_view



class Process_Merge(Process_Rewrite):
    __mapper_args__ = {'polymorphic_identity': 'process_merge'}
    def prepare_view(self):
        task_view = super(Process_Merge, self).prepare_view()

        n_minus_one=task_view["Context"]
        task_view["Context"]=""
        task_view["Body_Of_Task"]="_PREVIOUS PART_ " + task_view["Body_Of_Task"]+"" \
                                                                                 "                     _CURRENT PART_               " \
                                                                                 ""+n_minus_one+" ."


        return task_view

class Process_Merge_Alt_View(Process_Rewrite):
    __mapper_args__ = {'polymorphic_identity': 'process_merge_alt_view'}
    def prepare_view(self):
        task_view = super(Process_Merge_Alt_View, self).prepare_view()

        n_minus_one=task_view["Context"]
        task_view["Context"]=""
        task_view["Body_Of_Task"]="____________PREVIOUS PART__________ " + n_minus_one+"" \
                                                                                 " ________________CURRENT PART_________" \
                                                                                 ""+task_view["Body_Of_Task"]+" ."


        return task_view

class Content(Base):
    __tablename__ = 'content'
    id=Column('id', Integer, primary_key=True)
    origin_process_id = Column(Integer, ForeignKey('process_object.id'))  # who created it
    process_that_selected_this_content_id = Column(Integer, ForeignKey(
        'process_object.id'))  # If this process was selected by a process to passed forward, who was it

    user_id=Column(ForeignKey("user.name"))
    #user=relationship('User',foreign_keys=[user_id],uselist=False,back_populates="associated_content")

    content_type=Column('content_type', String) #the content to be parsed
    comments=Column('comments', String) # any notes
    results=Column('results',String) #the actual content the user entered

    created_date = Column(DateTime, default=datetime.datetime.now)  # base this function to evaluate at run time
    assigned_date = Column(DateTime) #when was data actually assigned ot the user
    completed_date = Column(DateTime)



    is_assigned=Column('is_assigned', Boolean, default=False)
    is_completed=Column('is_completed', Boolean, default=False)  # has the user finished this content - or this iteration
    is_locked=Column('is_locked', Boolean,default=False)  # can it be modified or edited


    origin_process=relationship("Process_Object",foreign_keys=[origin_process_id] ,backref="user_content_being_generated_from_this_process")


    process_that_selected_this_content = relationship("Process_Object", foreign_keys=[process_that_selected_this_content_id],
                                            backref="final_results")


    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    def get_completion_time(self):

        time_to_complete = (datetime.datetime.now() - self.assigned_date).total_seconds()
        return time_to_complete

    def __init__(self):
        self.is_completed = False
        self.is_locked = False
        self.results=""

    def __repr__(self):
        return "<ID {} Values {} isCompleted {}>".format(self.id,self.results,self.is_completed)

class Content_Result(Content): #like content but is specifically when it is the results of a system
    __mapper_args__ = {'polymorphic_identity': 'content_result'}


    linked_content_id = Column("linked_content_id", Integer, ForeignKey("content.id"))
    linked_content = relationship('Content',foreign_keys=[linked_content_id],uselist=False,viewonly=True)

    def __init__(self,value="",is_completed=False):
        super(Content_Result, self).__init__()
        self.is_locked=True #This cannot be sent out for work to be done on it
        self.is_completed=is_completed
        self.results=value


class Content_Types(object):
    Rate="Rate"
    Summarize="Summarize"
    Rewrite="Rewrite"
    Merge="Merge"
    Sugeest="Suggest"

if __name__ == '__main__':

    conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source")  # user='postgres', password='1234'
    Base.metadata.create_all(conn)

    cont1=Content()

    cont1.results="I am stalin"
    cont2 = Content()
    cont2.id=6626
    cont2.results = "modification of stalin"

    cont2.is_completed=True
    cont1.is_completed=True

    l = Task_Parameters(cont2)
    l2= Task_Parameters(cont1)

    d = Process_Object(cont1)


    t = Process_Object(cont2)
    #t.get_content_produced_by_this_process().append(cont2)
    t.get_content_produced_by_this_process().append(cont1)

    d.id=666

    session.add(t)
    session.add(d)

    t.initialize_user_content()
    #d.initialize_user_content(4,Process_Rate)
   # d.sub_process[0].get_final_results().append(cont1 )
    d.is_completed=False
    d.is_locked=False
    t.is_locked=False
    t.id=54

    session.add(l2)
    session.add(t)
    session.add(l)
    session.add(cont1)
    session.add(cont2)



    results=t.select_data_for_analysis(session)
    for j in results:
        print j[0].results
        print j[0].is_completed
    #results=t.select_data_for_analysis(session)
    print "HI "
    print results
    print "KHAN"
    # Get All PRocesses whose previous process is compelte and locked or null
    # Get All Processes whose task content are complete ( Can be analyzed)
    # Get All Context Who Parent Process Is NOt Locked Or Null (Parent is different from previous, parent refers to nested calls)
    # Unlock It

    # Get All Unlocked Processes
    # Get All Content Create From It. IsComplete
    # Assign Result

    # Get all unlcoked Processes
    # If Is Complete()
    # Locked It, Set It To Complete

    #Get Data To Calculate Results
    #For A Given Process Get All Subprocesses Results
    #IF There Are subprocesses involved ->
    first = session.query(Process_Object).filter(Process_Object.is_completed == False).filter(Process_Object.is_locked==False).subquery("first")
    second=session.query(Content).filter(Content.origin_process_id==first.c.id).subquery("second")
    third=session.query(Task_Parameters).filter(Task_Parameters.body_of_task_id==second.c.id).subquery("third")
    fourth=session.query(Process_Object).filter(Process_Object.task_parameters_id==third.c.id).subquery("fourth") #suprocesses
    fifth=session.query(Content).filter(Content.process_that_selected_this_content_id==fourth.c.id) #process_that_selected_this_content_id
    #six resutls are complete
    # (Body_Of_Task, ResultList), (Body_OF_Task, ResultList)
    #If not
    #Get content that is complete  (content, content)
    for j in fifth:
        print 'whut'
        print j.results
        print j
    '''
    t = Session.query(
        Posts.user_id,
        func.max(Posts.post_time).label('max_post_time'),
    ).group_by(Posts.user_id).subquery('t')

    query = Session.query(User, Posts).filter(and_(
        User.user_id == Posts.user_id,
        User.user_id == t.c.user_id,
        Posts.post_time == t.c.max_post_time,
    ))

    for user, post in query:
        print user.user_id, post.post_id
    '''


    first=session.query(Task_Parameters).filter(Task_Parameters.body_of_task_id==6626).subquery("first")

    second=session.query(Process_Object).filter(Process_Object.task_parameters_id==first.c.id)


    result=session.query(Process_Object ).filter(Process_Object.id==666)

    result=session.query(Process_Object).filter()
    temp=None
    for j in result:
        print j.get_content_produced_by_this_process()


    #if element has associated subprocess, then return (content, result), else return (content,content)
    #
    '''

    '''