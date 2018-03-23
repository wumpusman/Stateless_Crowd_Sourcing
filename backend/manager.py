from db_connection2 import *
import random
class Manager(object):
    remove_enum="remove" #corresponding enum  must be changed in frontend
    promote_enum="promote" #corresponding enum must be changed in frontend
    def __init__(self,session,max_time=7):
        # type: (object, object) -> object
        self.session=session
        self._session_time=max_time*60 #convert from minutes to seconds
        self._minimum_work_time=0 #seconds
        self._task_timeout_max=10 #This is in MINUTES
        self._effort_ratio=0
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
            self._unassign_content(relevant_content)


        self.session.commit();

    def _unassign_content(self,relevant_content):
        relevant_content.associated_user = None  # that user will no longer have that content associated with them
        relevant_content.is_completed = False
        relevant_content.results=""

    def edit_process(self,process,content,edit_msg,result_msg):
        '''

        :param process: associated process
        :param content: content from taht process
        :param edit_msg: type of edit to be done
        :param result_msg: the corresponding result of that content - it can be edited
        :return:
        '''
        was_effective=True
        if process.is_locked == False: #if the process can still be modified
            if edit_msg==Manager.remove_enum: #if we want to clear the work of one person because it sucked so hard
                self._unassign_content(content)

                sub_task_param=self.session.query(Task_Parameters).filter(Task_Parameters.result_id==content.id).all() #if this content was being evaluated in someway
                if len(sub_task_param) >0: #clear any ratings from it, this is garbage
                    rating_process=sub_task_param[0].parent_process
                    rating_process.is_locked=False
                    rating_stuff=rating_process.get_content_produced_by_this_process()
                    for rated_content in rating_stuff:
                        self._unassign_content(rated_content)
            #available_result_slots = self.get_final_results_incomplete(session).all()  # get results that are incomplete
            elif edit_msg==Manager.promote_enum: #this value will get assigned to whatever open final results that haven't been assigned, assuming there is one
                main_final_results=process.get_final_results_incomplete(self.session).all()
                if len(main_final_results)>0:
                   chosen_result= main_final_results[0]
                   chosen_result.linked_content=content
                   chosen_result.is_locked = True
                   chosen_result.is_completed = True
                   chosen_result.results=result_msg #if you choose to override the message with an alternate message
                if len(main_final_results) ==1: #only one remained
                    process.is_locked=True
                #just lock this particular content's associated subprocess
                sub_task_param = self.session.query(Task_Parameters).filter(Task_Parameters.result_id == content.id).all()
                if len(sub_task_param) >0:
                    rating_process = sub_task_param[0].parent_process
                    rating_process.lock_process()

        else:
            was_effective=False


        self.session.commit()
        return was_effective

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


                raise Exception("assigning new content when current content is not complete")


        optional_content = user.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self.session).all()


        #select all content where it was the top content
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

        get_user=lambda cont: str(cont.user_id)

        def get_score(content):
            try:
                return  session.query(Task_Parameters).filter(Task_Parameters.result_id == c.id).all()[
                    0].parent_process._calculate_score(session)
            except:
               return -1.0 #not a valid score yet


        user_input_and_id_and_associated_user=[(c.id,c.results,get_user(c),get_score(c)) for c in single_process.get_content_produced_by_this_process()]

        prompt=single_process.task_parameters_obj.prompt.results
        body=single_process.task_parameters_obj.body_of_task.results
        is_finished=single_process.is_locked;
        result_text = single_process.get_final_results()[0].results


        #get relevant information
        #processes and state
        zero=session.query(Task_Parameters).subquery('zero')
        first=session.query(zero,Content.is_completed.label('body_completed')).join(Content,Content.id==zero.c.body_of_task_id).subquery('first')
        second=session.query(first,Content.is_completed.label('result_completed')).join(Content,Content.id==first.c['result_id']).subquery('second')
        third=session.query(second,Content.is_completed.label('context_completed')).join(Content,Content.id==second.c['context_id']).subquery('third')
        fourth=session.query(third,Content.is_completed.label('prompt_completed')).join(Content,Content.id==third.c['prompt_id']).subquery('fourth')
        fifth=session.query(fourth,Content.is_completed.label('suggestion_completed')).join(Content,Content.id==fourth.c['suggestion_id']).subquery('fifth')
        sixth=session.query(fifth,Process_Rewrite.id.label("process_id"),Process_Rewrite.is_completed.label("p_complete"), Process_Rewrite.is_locked.label("p_locked"),
                            Process_Rewrite.is_completed.label('p_completed')).join(Process_Rewrite,Process_Rewrite.id==fifth.c.id).subquery('sixth')

        #get the count of associated child element
        seventh=session.query(sixth,Content.is_completed.label('c_completed')).join(Content, Content.origin_process_id ==sixth.c['process_id']).subquery('seventh')

        eight=session.query(seventh.c.process_id, func.count(seventh.c.c_completed).filter(seventh.c.c_completed==True).label('cont_comp')).\
            group_by(seventh.c.process_id).order_by(seventh.c.process_id).subquery('eight')


        nine=session.query(sixth,eight.c.cont_comp).join(eight,sixth.c.process_id==eight.c.process_id).order_by(eight.c.process_id).subquery("nine")

        col_ids=["process_id","p_complete","p_locked","cont_comp","body_completed","result_completed","context_completed","prompt_completed","suggestion_completed"]

        cols=[nine.c[col_id] for col_id in col_ids]
        ten=session.query (*cols ).all()
        is_ready_func = lambda ary: False if (False in ary[4:]) else True

        processes_and_state = []
        for ary in ten:
            ready = is_ready_func(ary)
            in_progress = True if ary[3] > 0 else False
            is_locked = ary[2]
            relevant={"is_finished": is_locked,
             "in_progress": in_progress,
             "process_id": ary[0],
             "is_ready":ready

             }
            processes_and_state.append(relevant)

        results={}
        results["processes_state"]=processes_and_state
        results["prompt"]=prompt
        #results["user_input"]=user_input
        results["content"]=user_input_and_id_and_associated_user
        results["is_finished"]=is_finished
        results["process_id"]=id
        results["body"]=body
        results["result"]=result_text

        return results

    def prepare_view(self,content): #calls content that created it, view state
        if type(content)==type(None):
            return {"Project_State":"Finished"}


        print content
        print content.origin_process

        view= content.origin_process.prepare_view()
        view["Project_State"]="Project" #we are still working on the proejct
        view["Session_Time"]=self._session_time
#
        return view
    def update_global_state(self,user,results):
        session=self.session

        current=user.get_current_content_in_progress(session)
        #Todo: This is sort of telling the system if person barely wrote anything to ignore it, need a better place to hold this code


        if isinstance(current.origin_process, Process_Rewrite): #
            if current.assigned_date !=None: #todo change this so that all values have an assigned date!
                print (datetime.datetime.now() - current.assigned_date).total_seconds()
                if (datetime.datetime.now() - current.assigned_date).total_seconds() < self._minimum_work_time:
    #
                    self.unassign_content(current)
                    return False


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
                  return False

              #if float(current.results)>=3:
              effective_effort=current.origin_process.get_expected_completion_read_ratio(current)

              if effective_effort<self._effort_ratio:

                      print "LAZY MAN"
                      self.unassign_content(current)
                      return False


        print "AND HERE"
        #ToDO:ANother HACK
        if current.results.replace(" ","") =="": #If user wrote nothign

            self.unassign_content(current)
            return

        current.is_completed=True
        current.completed_date=datetime.datetime.now()


        # Update the process and if it has a parent  process ASSIGN results I should change this
        current.origin_process.update_model(self.session) #update own model
        if current.origin_process._can_assign_result(self.session):

            current.origin_process.assign_result(session)

            if current.origin_process.parent_process != None:
                current.origin_process.parent_process.update_model(self.session) #update parent model
                if current.origin_process.parent_process._can_assign_result(self.session):
                    current.origin_process.parent_process.assign_result(session)

        #Do I freeze that component when it is done so don't waste resource s
        if current.origin_process.is_complete(session):
            current.origin_process.lock_process()
            if current.origin_process.parent_process != None:
                if current.origin_process.parent_process.is_complete(session):
                    current.origin_process.parent_process.lock_process()

        if current.origin_process.parent_process != None:
            current.origin_process.parent_process.update_model(self.session)

        self.session.commit()