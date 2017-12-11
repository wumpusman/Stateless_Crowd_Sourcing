from db_connection2 import *
class Manager:
    def __init__(self,session,max_time=7):
        # type: (object, object) -> object
        self.session=session
        self._session_time=max_time*60 #convert from minutes to seconds

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

        return self.prepare_view(current_user.associated_content[-1])

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


        #self.unassign_timeout_content()
        ##total_seconds()
        if len(user.associated_content)>0:
            if user.associated_content[-1].is_completed==False:
                return Exception("assigning new content when current content is not complete")
        optional_content = user.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self.session).all()


        results= self.session.query(Process_Object).all()

        #result=self.session.query(Process_Rate).all()

        '''
        print len(results)
        for i in results:

            if  i.parent_process == None:
                print i._can_assign_result(self.session)
                print i.task_parameters_obj.prompt.results
                print i.task_parameters_obj.body_of_task.results
                print str(i.get_content_produced_by_this_process()) + "CONTENT GENERATED FROM THIS PROCESS"
                print str(i.is_completed) + "is completed"
                print str(i.is_locked) + "is locked"
                print str(i.get_final_results_complete(self.session).all()[0]) + " Chosen element"

                chosen_one=i.get_final_results_complete(self.session).all()[0].linked_content_id


            else:
                print "score of a given result associated with the given prompt"
                print i.parent_process.task_parameters_obj.prompt.results
                print i.task_parameters_obj.result.results
                print str(i.get_content_produced_by_this_process())
                print str(i.get_final_results_complete(self.session).all()[0]) + " Chosen element"

        print "GREAT"
        '''
        #print self.session.query(Content).filter(Content.user_id!=None).filter(Content.is_completed==False).all()

        if len(optional_content)==0: return None
        chosen=optional_content[0]
        chosen.associated_user=user
        chosen.assigned_date=datetime.datetime.now()

        self.session.add(chosen)
        self.session.commit()
        return chosen

    def prepare_view(self,content): #calls content that created it, view state
        if type(content)==type(None):
            return {"Project_State":"Finished"}

        view= content.origin_process.prepare_view()
        view["Project_State"]="Project" #we are still working on the proejct
        view["Session_Time"]=self._session_time

        return view
    def update_global_state(self,user,results):
        session=self.session


        current=user.associated_content[-1]
        if isinstance(current.origin_process, Process_Rewrite):

            if (datetime.datetime.now() - current.assigned_date).total_seconds() < 15:
                print "THIS SHOULD NEVER BE CALLED"
                self.unassign_content(current)
                return
        # total_seconds()

        if(current.is_completed==True):
            return Exception("Content completed when it shouldn't be completed already")

        current.results= results["value"]
        #This is a hack :/\/\
        #TODO: This should be chagned and embedded, also the defualt for ratings should be different

        if isinstance(current.origin_process,Process_Rate):
              if current.origin_process.task_parameters_obj.result.results=="":
                  current.results="-2"
              if current.results=="" or current.results=="Enter Response Here":

                current.results="-2"
                current.comments="User wrote nothing"

        current.is_completed=True
        current.completed_date=datetime.datetime.now()

        #Update the process and if it has a parent any parent process
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