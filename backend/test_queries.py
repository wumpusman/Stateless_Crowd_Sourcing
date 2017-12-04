import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)  #reference parent directory
import unittest

from db_connection2 import *


def buildContent(value,id,is_complete=True):
    temp=Content()
    temp.results=value
    temp.is_completed=is_complete
    temp.id=id

    return temp






class Test_Queries(unittest.TestCase):

    def setUp(self):
        conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test")

        meta.drop_all(bind=conn)  # clear everything
        Base.metadata.create_all(conn)


        cont1_raw_data = buildContent("I want to be successful. But I don't know how", 10, True)
        cont2_prompt = buildContent("Rewrite the following text to make it more depressing", 11, True)
        cont3_context = buildContent("Arbitary context", 12, True)





        basic_process = Process_Text_Manipulation(body_of_task=cont1_raw_data, prompt=cont2_prompt, context=cont3_context,content_to_be_requested=0)

        basic_process.id = 666

        # Assign the relationships
        self.basic_process = basic_process
        self.session = session


        for i in xrange(2):  # 2 results
            text = "I'm a failure at everything I do, I'll never be successful"
            id = 20 + i
            cont = buildContent(text+str(id), id, True)
            sub_pr = Process_Rate(body_of_task=cont,displayed_result=cont, prompt=cont2_prompt, context=cont3_context,content_to_be_requested=0)

            basic_process.get_content_produced_by_this_process().append(cont)

            basic_process.sub_process.append(sub_pr)

        #hardcode EVEYRTHING BY HAND
        basic_process.minimum_amount_of_content_being_requested=3
        basic_process.sub_process[0].minimum_amount_of_content_being_requested=3
        basic_process.sub_process[1].minimum_amount_of_content_being_requested = 3

        # First sub_process_children
        sub_pr_cont11 = buildContent("1", 30, True)
        sub_pr_cont12 = buildContent("issue", 31, True)
        sub_pr_cont13 = buildContent("", 32, False)

        basic_process.sub_process[0].get_content_produced_by_this_process().append(sub_pr_cont11)
        basic_process.sub_process[0].get_content_produced_by_this_process().append(sub_pr_cont12)
        basic_process.sub_process[0].get_content_produced_by_this_process().append(sub_pr_cont13)

        # Second Sub Process Children
        sub_pr_cont21 = buildContent("5", 33, True)
        sub_pr_cont22 = buildContent("4", 34, True)
        sub_pr_cont23 = buildContent("5", 35, True)


        self.sub_pr_cont21=sub_pr_cont21


        basic_process.sub_process[1].get_content_produced_by_this_process().append(sub_pr_cont21)
        basic_process.sub_process[1].get_content_produced_by_this_process().append(sub_pr_cont22)
        basic_process.sub_process[1].get_content_produced_by_this_process().append(sub_pr_cont23)



        session.add(self.basic_process)

        #Lazy implicit way of getting eveyrthing 'added'
        session.query(Content).all()
        session.query(Task_Parameters).all()
        session.query(Process_Object).all()


    def test_select_queries(self):
        #self.setUp() #initialize the whole set up


        session=self.session



        sub_process1_length=self.basic_process.sub_process[0].select_data_for_analysis(self.session )
        sub_process2_length = self.basic_process.sub_process[1].select_data_for_analysis(self.session)

        get_self = session.query(Process_Object).filter(Process_Object.id == self.basic_process.id).subquery("get_self")

        get_content_stemming_from_this_process = session.query(Content).filter(
            Content.origin_process_id == get_self.c.id).filter(Content.is_completed == True).subquery(
            "get_content_stemming_from_this_process")



        tasks_associated_with_this_content = session.query(Task_Parameters).filter(
            Task_Parameters.body_of_task_id == get_content_stemming_from_this_process.c.id). \
            subquery("tasks_associated_with_this_content")

        processes_associated_with_this_task = session.query(Process_Object).filter(
            Process_Object.task_parameters_id == tasks_associated_with_this_content.c.id).subquery(
            "processes_associated_with_this_task")  # suprocesses



        relevant_results = session.query(Content).filter(
            Content.process_that_selected_this_content_id == processes_associated_with_this_task.c.id).filter(
            Content.is_completed == True).all()  # process_that_selected_this_content_id



        self.assertEqual(len(sub_process1_length),2,msg="The first subprocess should have only 2 compeleted data")
        self.assertEqual(len(sub_process2_length),3,msg="The second subprocess should have only 3 compeleted content/info return by user ")


        outcome= self.basic_process.task_parameters_obj.get_tasks_that_are_ready(session).all()

        self.assertEqual(outcome[0].body_of_task.results , "I want to be successful. But I don't know how",msg="The associated input to the first process")

        print outcome[1].body_of_task.results
        self.assertEqual(outcome[1].body_of_task.results, "I'm a failure at everything I do, I'll never be successful20",
                         msg="The associated input to both subprocesses")

        outcome=Process_Object.get_processes_that_are_ready(session).all()

        self.assertEqual(len(outcome),3,msg="There should be three processes associated with each of the tasks")

        self.basic_process.sub_process[0].task_parameters_obj.body_of_task.is_completed=False
        outcome = Process_Object.get_processes_that_are_ready(session).all()
        self.assertEqual(len(outcome), 2, msg="There should now only be two process that have their task parameters ready")


        self.basic_process.sub_process[0].task_parameters_obj.context.is_completed=False
        outcome = Process_Object.get_processes_that_are_ready(session).all()
        #print self.basic_process.sub_process[0].should_expand_user_requests(session)

        print self.basic_process.sub_process[0]._get_content_completed_counts(session)
        self.basic_process.sub_process[0].assign_result(session)

        session.rollback()

    def test_aacalculating_results(self):

        session = self.session
        self.assertEqual(self.basic_process.sub_process[1]._can_assign_result(session),True)
        self.assertEqual(self.basic_process.sub_process[0]._can_assign_result(session), False)


        #Calculating a score for one of one of the subprocesses, and updating resutls accordingly
        self.assertEqual(type(self.basic_process.sub_process[1].get_final_results()[0].results),type(None))
        self.basic_process.sub_process[1].assign_result(session)
        self.assertLess(float(self.basic_process.sub_process[1].get_final_results()[0].results)-4.66,.01, msg="was a score properly assigned")






        #Now lets see if the main process first has something to assign, and then after assigning a result, has now one thing completed and assigned
        self.assertEqual(len(self.basic_process.get_final_results_complete(session).all()), 0,
                         msg="should have no results aquired and assigned")
        self.assertEqual(len(self.basic_process.get_final_results_incomplete(session).all()), 1,
                         msg="should have 1 results unassigned")


        self.basic_process.assign_result(session)
        print self.basic_process.get_final_results_complete(session).all()
        self.assertEqual(len(self.basic_process.get_final_results_complete(session).all()),1,msg="should have one result acquired and assigned")




        #Now modify the other subprocess
        unclean_content=self.basic_process.sub_process[0].get_content_produced_by_this_process()
        for j in unclean_content:
            j.results="5"
            j.is_completed=True

        self.assertEqual(self.basic_process.sub_process[0]._can_assign_result(session), True)
        self.basic_process.sub_process[0].assign_result(session)

        self.assertEqual(self.basic_process.get_final_results_complete(session)[0].results,"I'm a failure at everything I do, I'll never be successful21")

        self.assertEqual(float(self.basic_process.sub_process[0].get_final_results()[0].results), 5,
                        msg="was a score properly assigned")



        session.rollback()

    def test_content_assignment_to_user(self):

        session=self.session

        t=User("generic user")
        t.associated_content.append(self.basic_process.get_content_produced_by_this_process()[0])
        result = t.get_all_processes_where_user_was_uninvolved(session).all()
        self.assertEqual(len(result),2,msg="should have two processes i haven't engaged with")

        print t.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()
        self.assertEqual(len(t.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()), 1,
                         msg="only one content is currently unlocked and unassigned")

        self.sub_pr_cont21.is_completed = False

        self.assertEqual(len(t.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()), 2,
                         msg="two pieces of content is currently unlocked and unassigned")

        self.basic_process.sub_process[0].is_locked=True
        self.sub_pr_cont21.is_completed = True

        self.assertEqual(len(t.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()), 0,
                         msg="no pieces content is currently available for assignment")



        t.associated_content.append(self.basic_process.sub_process[0].get_content_produced_by_this_process()[0])
        result = t.get_all_processes_where_user_was_uninvolved(session).all()
        self.assertEqual(len(result), 1, msg="should have one processes i haven't engaged with")

        session.rollback()




    def test_assignment_and_update_process(self):
        session=self.session

        #First free the previous processes that existed
        result=session.query(Process_Object).filter(Process_Object.is_locked==False).all()
        self.assertEqual(len(result),3)
        self.basic_process.lock_process()
        result = session.query(Process_Object).filter(Process_Object.is_locked == False).all()
        self.assertEqual(len(result), 0)


        session.rollback() #ERase everything



        user1=User("Joe")
        user2=User("John")

        body_of_task=Content_Result("I love going skiiing",is_completed=True)
        prompt=Content_Result("Write the following sentence to make it sound more negative",is_completed=True)
        context=Content_Result("A person is talking about their exciting skii trip",is_completed=True)
        suggestions=Content_Result("",is_completed=True)


        sub_process_info={"prompt":Content_Result("Rate how well the revised content sounds more negative, as well as overall better than the original",
                          is_completed=True),
                          "context":body_of_task,
                          "content_to_be_requested":1,
                          "expected_results":1
                          }



        first_rewrite_process = Process_Rewrite(body_of_task, prompt, context, suggestions, content_to_be_requested=2,subprocess_tuple=(Process_Rate,sub_process_info))

        session.add(first_rewrite_process)

        results= user1.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()

        self.assertEqual(results[0].origin_process_id,results[1].origin_process_id,msg="Should be only one origin process")

        user1.associated_content.append(results[0])

        results[0].results="I kinda like skiing, it's ok"
        results[0].is_completed=True

        self.assertEqual(first_rewrite_process._can_assign_result(session),False)

        result = user2.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()
        print result[0].origin_process
        print result[1].origin_process
        print type(result[1].origin_process)==Process_Rewrite
        result = [j for j in result if type(j.origin_process) == Process_Rewrite]

        result[0].associated_user = user2

        result[0].results = "Skiiing fucking sucks"
        result[0].is_completed = True



        relevant_content= user2.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()[1]



        self.assertEqual(user2.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(session).all()[0].origin_process.task_parameters_obj.result.results,
                         "I kinda like skiing, it's ok")
        self.assertEqual(user1.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(session).all()[
                             0].origin_process.task_parameters_obj.result.results,
                         "Skiiing fucking sucks")

        self.assertEqual(relevant_content.origin_process._can_assign_result(session),False)

        user2.associated_content.append(relevant_content)
        relevant_content.results="5"
        relevant_content.is_completed=True

        self.assertEqual(relevant_content.origin_process._can_assign_result(session), True)
        relevant_content.origin_process.assign_result(session)

        result = user1.get_all_unassigned_and_available_content_where_user_was_uninvolved(session).all()


        result[0].results = "issue"
        result[0].is_completed = True
        result[0].origin_process.assign_result(session)

        first_rewrite_process.assign_result(session)

        first_rewrite_process.get_final_results_complete(session).all()[0].results



        session.rollback()
    @staticmethod
    def lazyAssign(element,text_resp,num):

        if str(type(element.origin_process))=="<class 'backend.db_connection2.Process_Rate'>":
            element.results=str(num)
        else:
            element.results=text_resp

        element.is_completed=True



    def test_full_iteration(self):

        session=self.session
        #First free the previous processes that existed
        result=session.query(Process_Object).filter(Process_Object.is_locked==False).all()
        self.assertEqual(len(result),3)
        self.basic_process.lock_process()
        result = session.query(Process_Object).filter(Process_Object.is_locked == False).all()
        self.assertEqual(len(result), 0)

        session.rollback()  # ERase everything

        User1=User("Michael")
        User2=User("Joe")
        User3=User("Bob")


        body_of_task = Content_Result("I love going skiiing", is_completed=True)
        prompt = Content_Result("Write the following sentences to make them sound more negative", is_completed=True)
        context = Content_Result("I love my life in america", is_completed=True)
        suggestions = Content_Result("", is_completed=True)

        sub_process1_info = {"prompt": Content_Result(
            "Rate how well the revised content sounds more negative, as well as overall better than the original",
            is_completed=True),
                            "context": body_of_task,
                            "content_to_be_requested": 2,
                            "expected_results": 1
                            }


        first=Process_Rewrite(body_of_task,prompt,context,suggestions,expected_results=1,content_to_be_requested=3,subprocess_tuple=(Process_Rate,sub_process1_info))



        second=Process_Rewrite(first.get_final_results()[0],prompt,context,suggestions,expected_results=1,content_to_be_requested=2,subprocess_tuple=(Process_Rate,sub_process1_info))

        prompt_suggestion = Content_Result(
            "Provide suggestions on you would change or edit this text to make it sound more negative",
            is_completed=True)
        sub_process_suggestion_info = {
            "prompt": Content_Result(
                "Rate how well you feel the suggestions would make this text sound more negative, and better in general",
                is_completed=True),
            "context":second.get_final_results()[0],
            "content_to_be_requested":1,
            "expected_results":1
            }


        third=Process_Text_Manipulation(second.get_final_results()[0],prompt_suggestion,context,suggestions,expected_results=1,
                                        content_to_be_requested=2,subprocess_tuple=(Process_Rate,sub_process_suggestion_info))


        session.add(first)
        session.add(second)
        session.add(third)

        import random

        suggestion_mapping={User1:("I think America is great",""),User2:("I think my life isn't great tbh",5),User3:("I think things are fucking awful atm",4)}

        userList=[User1,User2,User3]
        for counter in xrange(10):

            for user in userList:

                optional_content = user.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self.session).all()
                if len(optional_content)==0: continue

                chosen=optional_content[0]
                chosen.associated_user=user
                self.lazyAssign(chosen,suggestion_mapping[user][0],suggestion_mapping[user][1])
                chosen.origin_process.assign_result(session)

                if chosen.origin_process.parent_process!=None:
                    chosen.origin_process.parent_process.assign_result(session)


                if chosen.origin_process.is_complete(session):
                    chosen.origin_process.lock_process()
                    if chosen.origin_process.parent_process != None:
                        if chosen.origin_process.parent_process.is_complete(session):
                            chosen.origin_process.parent_process.lock_process()



        self.assertEqual(first.get_final_results()[0].is_completed,True)
        self.assertEqual(second.get_final_results()[0].is_completed, True)
        self.assertEqual(third.get_final_results()[0].is_completed, True)

        fir=session.query(Task_Parameters).filter(first.get_final_results()[0].linked_content.id==Task_Parameters.body_of_task_id).subquery()
        sec=session.query(Process_Object).filter(fir.c.id==Process_Object.task_parameters_id).all()
        #print sec[0].get_final_results()[0].results



        session.rollback() #ERase everything


    #Select All Processses That are not locked
    #Select All Processes That'S Task_Parameters Is Complete

    #Get Current Data
    #Calculate Results
        #If Elemetns is < 3
        # NO UPDATE
        #ELSE
        #For Rating One
        #Float(Result)
        #Else Nan
        #If Nan > 2
        #Assign Score Lock Element Is complete = True
        #Else Average others
        #Assign Score To Result
        #Result.is_complete  =True
        #Lock Process

    #Get All Processes that are unlocked, that have content that is not locked, assign that content
    #If Found Result > 4
        #Lock Process



    #Assign Task
        #If User Already Assigned, Return Current Task
        #Else
        # Select All Processses That are not locked
        # Select All Processes That'S Task_Parameters Is Complete
        # Select All Content That Is Not Complete And Does Not have a User,
        # Get All Content that's Task_Parameter.body_of_task_id != 
        #Naive, pick one at random
        #



