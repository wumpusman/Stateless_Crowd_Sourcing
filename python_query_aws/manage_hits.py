
'''
Used to manage hits
'''
from env_info import Environment_Info
from datetime import datetime
from xml.dom.minidom import parseString
import boto3

#notify_workers
class Manage_Project(object):
    #A simple holder to link a project and the hits - This would definitely be linked to Database
    def __init__(self):
        self.project_id="Test_Projet"
        self._minimum_work_needed=10 # a fixed amount of task units left
        self._currently_assigned=10 #the number of assignemtns that have not been sent out
        self._last_time_work_was_done=datetime(2000,1,1) # Last Time People did actual work - i.e. do we need to request
                                                      #I actually have the right format in a diffenret ifle look it up
        self.threshold_to_make_a_new_hit=6
        self.longest_waiting_time=10 #what is maximum waiting time
        self.list_of_associated_hits=set()
        self.list_live_hits=set()

        self._dict_of_project_parameters={} #Just look at Environment env


    def get_live_hits(self):
        return list(self.list_live_hits)


    def create_hits(self,client):
        self._currently_assigned=self._minimum_work_needed
        result=Environment_Info.make_test_hit(client,max_assignments=self._minimum_work_needed)
        self.clear_live_hits(client)  # clear what ever was previous being done
        hit_id=result['HIT']['HITId']

        self.list_live_hits.add(hit_id)
        self._last_time_work_was_done=datetime.now()

    def clear_live_hits(self,client):
        for hit_id in self.list_live_hits:
            Environment_Info.delete_hit_quick(client,hit_id)

        self.list_live_hits=set() #should be more if this linked to a db :X


    def is_hit_part_of_this_project_and_active(self, hit_id):
        return hit_id in self.list_live_hits

    def get_hit_ui_design(self):
        '''
        It's just a link to the XML web that people will see
        :return:
        '''
        return Environment_Info.get_test_task_layout()


    def check_if_done(self):
        return False

    def update_project_state(self,last_task_succeeded): #update how much work needs to be done, and last time project was successfully updated
        if last_task_succeeded == True:
            self._currently_assigned-=1
            self._minimum_work_needed-=1 #less work needs to be done
            self._last_time_work_was_done=datetime.now()
        else:
            self._currently_assigned-=1

    def should_create_a_new_hit(self):
        if self._waiting_too_long():
            return True
        if self.number_additional_assignments_to_create() > self.threshold_to_make_a_new_hit:
            return True

        return False

    def number_additional_assignments_to_create(self):
        return self._minimum_work_needed - self._currently_assigned


    def _waiting_too_long(self):
        current_time = datetime.now() - self._last_time_work_was_done
        if current_time.days > self.longest_waiting_time:
            return True
        return False

    @staticmethod
    def static_get_associated_project(self, hit_id):
        return Manage_Project._test_get_associated_project(hit_id)

    @staticmethod
    def _test_get_associated_project(self,hit_id):
        return None




class Manage_Hits(object):
    def __init__(self,client):
        pass
        self.client=client  #client connected to relevant Account
        self.registry_id=None #not sure what this will be

    @staticmethod
    def static_notify_hit_availability(client,user_list, msg, hit_id):
        pass
        # A2ECVVX9WHBDRT
        # 341H3G5YF0FXE0MZ1W2GJC5KAAK0ZD

    @staticmethod
    def _test_read_open_hits(self): #list of open hits
        return []

    def read_open_hits(self): #list of open hits
        return Manage_Hits._test_read_open_hits()

    def read_hits(self,type=''): #list of hits, open or closed regardless
        return []

    def request_info(self,hit_id):
        return Environment_Info.request_hit_results(self.client,hit_id)


    def judge_survey_code(self,code):
        '''
               Answers if the survey code is correct or not - compared to some metric that determines if not - probably project based
               :param self:
               :return:
               '''
        return self._test_judge_survey_code(code)

    def _test_judge_survey_code(self,code):
        if code=='True': return True
        return False

    def _test_parse_user(self):
        return {'user_turk_id':"Mecha_Shiva" ,"survey_response":"the end is neigh pony...Fake Street"}

    def _parse_user_result(self, assignment): #parse results of a given user



        worker_id = assignment['WorkerId']
        assignment_id = assignment['AssignmentId']
        answer_xml = parseString(assignment['Answer'])

        # the answer is an xml document. we pull out the value of the first
        # //QuestionFormAnswers/Answer/FreeText
        answer = answer_xml.getElementsByTagName('FreeText')[0]
        # See https://stackoverflow.com/questions/317413
        only_answer = " ".join(t.nodeValue for t in answer.childNodes if t.nodeType == t.TEXT_NODE)


        return only_answer

    def get_user_results_that_need_to_be_approved(self,hit_id,max_results=999):
        results_to_be_approved=Environment_Info.request_hit_results(self.client,hit_id=hit_id,hit_types=["Submitted"],max_return=max_results)

        return results_to_be_approved

    def _update_mturk_account_generic(self,assignment_id,succeeded,comments=""):
        '''
        This used to updated, withOUT deep thought into issues of when they do a acceptable_users or bad_users job, how feedback should be done
        This function should be wrapped in another object that is context dependent
        :param assignment_id:  str what is being updated
        :param succeeded: bool if it failed or succeed
        :return:
        '''
        client = self.client

        if succeeded:
            client.approve_assignment(
                AssignmentId=assignment_id,
                RequesterFeedback=comments,
                OverrideRejection=False,
            )
        else:  # if failed
            client.reject_assignment(
                AssignmentId=assignment_id,
                RequesterFeedback='one or more your answers was rated too many stds form the norm of other users'

            )


    def update_mturk_assignments(self, assignment_id, succeeded):
        return self._update_mturk_account_generic(assignment_id,succeeded)



    def flow(self,project):



        single_project=project# faux project to handle stuff


        list_of_users_and_result=[] #Tuple, HitID, assignment_id user_name if they succeeded, comments {hit_id,user_name,succeeded,comments=''}

        open_hits=single_project.get_live_hits() #list all hits related ot this single project however that is done

        for hit in open_hits:
            hit_id=hit

            important_info=client.get_hit(HITId=hit_id)

            results_to_be_evaluated=self.get_user_results_that_need_to_be_approved(hit)
            print "MADE IT HERE AT LEAST?"
            for result in results_to_be_evaluated['Assignments']:
                print result
                assignment_id=result["AssignmentId"]

                survey_response=self._parse_user_result(result)
                user_id=result['WorkerId']

                succeeded=self.judge_survey_code(survey_response)



                individual_user_results=hit_id,assignment_id,user_id,succeeded,'this is just to test out the flow '



                if single_project.is_hit_part_of_this_project_and_active(hit_id): #probably project would be used for metric in updat
                    self.update_mturk_assignments(individual_user_results[1], individual_user_results[2])

                    single_project.update_project_state(succeeded)



                else:
                    Exception("hit being updated is not part of the current project ")

                #list_of_users_and_result.append(individual_user_results)



        if single_project.should_create_a_new_hit():
            single_project.create_hits(self.client)
            #close out all previous projects related to this project




if __name__ == '__main__':
    session = boto3.Session(profile_name=None)
    keys = Environment_Info.static_get_special_code()
    client = session.client(
        service_name='mturk',
        region_name='us-east-1',
        endpoint_url=Environment_Info.environments["sandbox"]['endpoint'],
        aws_access_key_id=keys["aws_access_key_id"],
        aws_secret_access_key=keys["aws_secret_access_key"] #' #
        # aws_session_token=SESSION_TOKEN,
    )
    p = Manage_Project()
    response = client.list_hits(

        MaxResults=100
    )

    #print response["HITs"][0]

    #print Environment_Info.environments["sandbox"]['preview'] + "?groupId={}".format(latestTask)

    print response

    #client.notify_workers(Subject="Requested Hit",MessageText="Your previous work on my tasks were pretty acceptable_users, and were rated 1.5 stds above the norm. I'm linking "
     #                                                         "another task with a higher pay amount that links to my project  ",WorkerIds=["A2ECVVX9WHBDRT"])
    # A2ECVVX9WHBDRT
    # 341H3G5YF0FXE0MZ1W2GJC5KAAK0ZD
    ''' 
    p=Manage_Project()
    m_h=Manage_Hits(client)
    while True:
        print p.get_live_hits()
        if len(p.get_live_hits())>00:

            hit_info= client.get_hit(HITId=p.get_live_hits()[0])

            print Environment_Info.environments["sandbox"]['preview']+"?groupId={}".format(hit_info["HIT"]["HITTypeId"])

        m_h.flow(p)
        raw_input(" Another go?")
    '''