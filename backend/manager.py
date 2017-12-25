from db_connection2 import *
import random
class Manager(object):
    def __init__(self,session,max_time=7):
        # type: (object, object) -> object
        self.session=session
        self._session_time=max_time*60 #convert from minutes to seconds
        self._minimum_work_time=20 #seconds
        self._task_timeout_max=10 #This is in MINUTES
    #I hate that i have to make this function each time someone queries the db :(

    def unassign_timeout_content(self,default_timeout=10):

        current_time_minus_X=datetime.timedelta(minutes=default_timeout)
        current_time_minus_X = datetime.datetime.now() - current_time_minus_X

        r=self.session.query(Content).filter(Content.user_id!=None).filter(Content.is_completed==False)

        content_not_completed_yet=r.filter(Content.assigned_date<current_time_minus_X).all()

        for non_completed in content_not_completed_yet:

            self.unassign_content(non_completed)

    def unassign_content(self,relevant_content):
        if relevant_content.is_completed==False:
            relevant_content.associated_user = None #that user will no longer have that content associated with them
            relevant_content.is_completed=False
        self.session.commit();


    def request_current_task(self,name,password):
        password = str(password)
        if self.does_user_exist(name) == False:
            self.create_user(name, password)

        current_user = self.select_user(name, password)

        if len(current_user.associated_content)==0: return self.prepare_view(None)

        return self.prepare_view(current_user.get_current_content_in_progress(session))

    def update_model(self,name,password,results):
        password=str(password)
        current_user = self.select_user(name, password)
        self.update_global_state(current_user, results)  # Update user state, update all the content


    def assign_new_content_to_user(self,name,password):
        password=str(password)
        current_user = self.select_user(name, password)
        self.assign_new_content(current_user)

    #does the full shebang
    def update_after_submitting_content(self,name,password,results): #assumes they have content that needs to be updated
        password=str(password)
        if self.does_user_exist(name)==False:
           self.create_user(name,password)



        current_user=self.select_user(name,password)

        if (len(current_user.associated_content))>0:

            self.update_global_state(current_user,results)  #Update user state, update all the content


        content=self.assign_new_content(current_user)
        view_dictionary=self.prepare_view(content)

        return view_dictionary

    def does_user_exist(self,name):
        result=self.session.query(User).filter(User.name==name).all()
        if len(result)==0:
            return False
        return True

    def select_user(self,name,password):
        try:
            return self.session.query(User).filter(User.name==name).filter(User.password==password).all()[0]
        except:
            return None


    def create_user(self,name,password):
        user=User(name)
        user.password=password
        self.session.add(user)
        self.session.commit()

    def assign_new_content(self,user):
        session = self.session


        all_rating=session.query(Process_Rate).all()


        self.unassign_timeout_content(self._task_timeout_max)
        ##total_seconds()
        if len(user.associated_content)>0:
            if user.get_current_content_in_progress(session)!=None:
                return Exception("assigning new content when current content is not complete")
        optional_content = user.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self.session).all()


        results= self.session.query(Process_Object).all()



        if len(optional_content)==0: return None

        chosen=random.choice(optional_content) #pick one of them but make the order inconsistent it's a fuck you to slackers, they'll be stuck in
        #an endless loop of dealing with bs


        chosen.associated_user=user
        chosen.assigned_date=datetime.datetime.now()


        self.session.add(chosen)

        self.session.commit()

        print user.name
        print user.associated_content
        print "THIS IS LINKED TO THIS USER"
        return chosen

    def prepare_results(self,id):

        session = self.session
        if id ==-1:
            id = session.query(Process_Text_Manipulation.id).all()[0][0]



        main_query=session.query (Process_Text_Manipulation).filter(Process_Text_Manipulation.id==id)
        single_process=main_query.all()[0]


        id=single_process.id
        user_input=[c.results for c in single_process.get_content_produced_by_this_process()]
        prompt=single_process.task_parameters_obj.prompt.results
        body=single_process.task_parameters_obj.body_of_task.results
        is_finished=single_process.is_locked;
        result_text = single_process.get_final_results()[0].results

        get_all_processes=session.query(Process_Text_Manipulation).all()

        processes_and_state=[{"is_locked":process.is_locked,"process_id":process.id } for process in get_all_processes]

        #Select All Rewrite processes
        #select All processes where ID > Previous
        #select first
        ''''
                  this.prompt=data["prompt"];
              this.result=data["result"];
              this.body=data["body"];
              this.user_inputs=data["user_input"];
              this.is_finished=data["is_finished"];
              this.process_id=data["process_id"];

        '''
        results={}
        results["processes_state"]=processes_and_state
        results["prompt"]=prompt
        results["user_input"]=user_input
        results["is_finished"]=is_finished
        results["process_id"]=id
        results["body"]=body
        results["result"]=result_text
        return results

    def prepare_view(self,content): #calls content that created it, view state
        if type(content)==type(None):
            return {"Project_State":"Finished"}

        view= content.origin_process.prepare_view()
        view["Project_State"]="Project" #we are still working on the proejct
        view["Session_Time"]=self._session_time

        return view
    def update_global_state(self,user,results):
        session=self.session

        current=user.get_current_content_in_progress(session)
        #Todo: This is sort of telling the system if person barely wrote anything to ignore it, need a better place to hold this code
        print current.origin_process

        if isinstance(current.origin_process, Process_Rewrite):

            print (datetime.datetime.now() - current.assigned_date).total_seconds()
            if (datetime.datetime.now() - current.assigned_date).total_seconds() < self._minimum_work_time:

                self.unassign_content(current)
                return


        # total_seconds()
        print "MADE IT HERE AS WELL!!"
        if(current.is_completed==True):
            return Exception("Content completed when it shouldn't be completed already")

        current.results= results["value"]
        #This is a hack :/\/\/\:
        #TODO: This should be chagned and embedded, also the defualt for ratings should be different

        if isinstance(current.origin_process,Process_Rate):
              if current.origin_process.task_parameters_obj.result.results=="":
                  self.unassign_content(current)
                  return

              #if float(current.results)>=3:
              effective_effort=current.origin_process.get_expected_completion_read_ratio(current)

              if effective_effort<1:

                      print "LAZY MAN"
                      self.unassign_content(current)
                      return


        print "AND HERE"
        #ToDO:ANother HACK
        if current.results.replace(" ","") =="": #If user wrote nothign

            self.unassign_content(current)
            return

        current.is_completed=True
        current.completed_date=datetime.datetime.now()

        #Update the process and if it has a parent  process
        if current.origin_process._can_assign_result(self.session):
            current.origin_process.assign_result(session)
            if current.origin_process.parent_process!=None and  current.origin_process.parent_process._can_assign_result(self.session):
                current.origin_process.parent_process.assign_result(session)

        #Do I freeze that component when it is done so don't waste resource s
        if current.origin_process.is_complete(session):
            current.origin_process.lock_process()
            if current.origin_process.parent_process != None:
                if current.origin_process.parent_process.is_complete(session):
                    current.origin_process.parent_process.lock_process()

        self.session.commit()