from db_connection2 import *
import random
class Manager(object):
    remove_enum="remove" #corresponding enum  must be changed in frontend
    promote_enum="promote" #corresponding enum must be changed in frontend

    issue_enum="Flagged" #something is wrong with a particular content

    user_good_enum="acceptable"
    user_bad="Bad_User"
    def __init__(self,session,max_time=7):
        # type: (object, object) -> object
        self.session=session
        self._session_time=max_time*60 #convert from minutes to seconds
        self._minimum_work_time=0 #seconds
        self._task_timeout_max=.1 #This is in MINUTES
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
        relevant_content.comments=""

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
                content.associated_user.alias = Manager.user_bad
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
                if len(main_final_results) ==1: #only one remained, then lock everything else
                    process.lock_process()
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


        if current_user.alias==Manager.user_bad:
            return self.prepare_view(current_user.alias) #pass the bad alias

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



    #assign new content
    #check examples
    #from new content - see if any examples DO those instead
    #else do normal content
    #

    def assign_new_content(self,user):


        session = self.session


        all_rating=session.query(Process_Rate).all()


        self.unassign_timeout_content(self._task_timeout_max)
        ##total_seconds()


        if len(user.associated_content)>0:


            if user.get_current_content_in_progress(session)!=None:


                raise Exception("assigning new content when current content is not complete")


        all_content = user.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self.session).subquery()# .all()
        #pick all content tat use r is not involved in




        #pick out those that are relevant
        relevant_ids=session.query(all_content.c.id).all()
        relevant_ids=[i[0] for i in relevant_ids] #my lazy way to ensure that I don't do a full search, get all the relevant id's


        #get by number completed
        result = session.query(all_content.c.is_completed, all_content.c.id.label("relevant_id"),
                               all_content.c.origin_process_id.label("relevant_process_id"), Process_Rate.id).join(
            Process_Rate, Process_Rate.id == all_content.c.origin_process_id).subquery()

        result2 = session.query(Content.origin_process_id, Content.is_completed).filter(
            result.c.relevant_process_id == Content.origin_process_id).subquery()

        result6 = session.query(result2.c.origin_process_id,
                                func.count(1).filter(result2.c.is_completed).label("count")).group_by(
            result2.c.origin_process_id).subquery()

        result7 = session.query(all_content.c.id, result6.c.count).join(result6,
                                                                        all_content.c.origin_process_id == result6.c.origin_process_id).order_by(
            result6.c.count).subquery()

        rate_option_sub_query= session.query(Content).filter(result7.c.id == Content.id).filter(
            Content.content_type == "").subquery('temp')


        rate_options = session.query(Content).filter(result7.c.id==Content.id).filter(Content.content_type=="").all()
        rewrite_options = session.query(all_content.c.id, all_content.c.origin_process_id).filter(
            Process_Rewrite.id == all_content.c.origin_process_id).subquery()

        rewrite_processes = session.query(Process_Rewrite.id).filter(Process_Rewrite.is_locked == False).all()

        rewrite_options = session.query(Content).filter(rewrite_options.c.id == Content.id).filter(
            rewrite_options.c.origin_process_id.in_(rewrite_processes)).filter(
            Content.content_type == "").all()

        '''            
            result=session.query(all_content.c.origin_process_id,Process_Rate_Flex.task_parameters_id,Process_Rate_Flex.current_score).join(Process_Rate_Flex,Process_Rate_Flex.id == all_content.c.origin_process_id).distinct().subquery()
            result2=session.query(Task_Parameters.result_id.label('result_id'),result).join(result,result.c.task_parameters_id==Task_Parameters.id).distinct().subquery()
            result3=session.query(Content.id,result2.c.current_score).join(result2,Content.id==result2.c.result_id ).distinct().order_by(result2.c.current_score).all()
        '''


        optional_content = session.query(Content).filter(Content.id.in_(relevant_ids)).filter(
            Content.content_type == "").all()
        #Content which does not have a specified type, which should by default be NONE

        testing_content=session.query(Content).filter(Content.id.in_(relevant_ids)).filter(Content.content_type==Content_Types.Testing_Enum).all() #Example content
        #Content that is used for testing or is example content


        problems_flagged=session.query(Content.comments).filter(Content.user_id ==user.name).filter(Content.comments==Manager.issue_enum ).all()
        #Is there any content wher ethere are issues





        if len(problems_flagged)>0:
            #bad form but eh
            return Manager.issue_enum #If they have fucked up on content

        if len(optional_content)==0: return None

        chosen=None




        is_good_user = True if user.alias==Manager.user_good_enum else False

        if len(testing_content)>0 and (is_good_user==False): #go through all the test contnet
            chosen=testing_content[0]

        else: #Lets look at cotnent


            if len(rewrite_options)>0:
                user.alias=Manager.user_good_enum #to make it here they have to be a good user
                chosen=random.choice(rewrite_options) #pick one of them but make the order inconsistent it's a fuck you to slackers, they'll be stuck in

            elif len(rate_options)>0: #choose the content that is closest to be finished

                chosen=self._select_content_on_score(session,rate_option_sub_query)
                if chosen ==None:
                    chosen=rate_options[-1]

                user.alias=Manager.user_good_enum  #to make it here they have to be a good user
            else: return None
        #an endless loop of dealing with bs

        print "WHAT IN THE FUCK IS GOING ON"
        chosen.associated_user=user
        chosen.assigned_date=datetime.datetime.now()


        self.session.add(chosen)

        self.session.commit()

        return chosen




    def _select_content_on_score(self,session,rate_option_sub_query):
        #assign contnet that are not locked that have highest score
        #select a unassigned content form that one


        sub_process=session.query(Process_Rate_Flex).filter(rate_option_sub_query.c.origin_process_id==Process_Rate_Flex.id).order_by(Process_Rate_Flex.current_score)[-1]
        front_running_process_to_evaluate_content=session.query(Content).filter_by(origin_process_id=sub_process.id,is_completed=False).all()
        if len(front_running_process_to_evaluate_content) >0:

            return front_running_process_to_evaluate_content[0]
        return None

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

        if content == Manager.issue_enum:
            return {"Project_State":Manager.issue_enum}

        if content==Manager.user_bad:
            return {"Project_State": Manager.user_bad}


        view= content.origin_process.prepare_view()
        view["Project_State"]="Project" #we are still working on the proejct
        view["Session_Time"]=self._session_time
#
        return view

    def update_global_state(self,user,results):
        session=self.session

        current=user.get_current_content_in_progress(session)
        #Todo: This is sort of telling the system if person barely wrote anything to ignore it, need a better place to hold this code


        if current ==None: #another hack
            return False

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

        if (current.origin_process.is_user_content_acceptable(current) == False):
            current.comments = Manager.issue_enum  # flag this content as unacceptable Or having a serious problem
            user.alias=Manager.user_bad                                 #THIS IS SUCH BAD FORM BUT WHATEVER AT THIS POITN
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

        #Do I freeze that component and associated processes  when it is done so don't waste resource s
        self._conditionally_lock_process(current)

        self.session.commit()


    def _conditionally_lock_process(self,current_element):
        current=current_element
        session=self.session
        if current.origin_process.is_complete(session):
            current.origin_process.lock_process()
            if current.origin_process.parent_process != None:
                if current.origin_process.parent_process.is_complete(session):
                    current.origin_process.parent_process.lock_process()

        if current.origin_process.parent_process != None:
            current.origin_process.parent_process.update_model(self.session)
