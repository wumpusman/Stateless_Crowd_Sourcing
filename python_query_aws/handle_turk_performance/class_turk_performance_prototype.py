class Turk_Performance_Prototype(object):
    def __init__(self,client,session):
        self.msg_for_rejection=""
        self.list_of_disqualifying_states=[]
        self.threshold_for_completion=999999
        self.actions_to_take_for_disqualification=[] #a functional list of operations to take in response to failure of a user for a specific task
                                #each should be a dict with a function, and parameters {"function":, "parameters":}
        self.actions_to_take_for_qualification=[]

        self.client=client #client to aws
        self.db_session=session #db_session

        self.set_default_actions({},{}) #define what actions shuould happen

    def set_default_actions(self,good_user_params,bad_user_params):
        self.actions_to_take_for_qualification=[]
        self.actions_to_take_for_disqualification=[]
        self.actions_to_take_for_disqualification.append({"function": self._reject_work, "parameters": {}})
        self.actions_to_take_for_disqualification.append({"function": self._block_user, "parameters": {}})
        self.actions_to_take_for_disqualification.append({"function": self._label_bad, "parameters": {}})

        self.actions_to_take_for_qualification.append({"function": self._accept_work, "parameters": {}})


    def should_disqualify_user(self,user_state,relative_time, user_exists):
        #returns decision, and

        should_disqualify=False
        reason=""
        msg=""

        if user_exists==False:
            should_disqualify=True
        if relative_time>self.threshold_for_completion:
            should_disqualify=True
        if user_state in self.list_of_disqualifying_states:
            should_disqualify=True

        if should_disqualify:
            msg=self.msg_for_rejection

        decision={"should_disqualify":should_disqualify,"reason":reason,"msg":msg}


        return decision


    def logic(self,user_state, relative_time, user_exists):

        decision=self.should_disqualify_user(user_state,relative_time,user_exists)

        if decision["should_disqualify"]:
            for function_dict in self.actions_to_take_for_disqualification:
               function= function_dict["function"]
               parameters=function_dict["parameters"]

               function(**parameters) #call actions to take
        else:
            for function_dict in self.actions_to_take_for_qualification:
                function = function_dict["function"]
                parameters = function_dict["parameters"]

                function(**parameters) #call actions to take if they did good



    def _update_mturk_account(self,assignment_id,succeeded,comments=""):
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
                RequesterFeedback=self.msg_for_rejection

            )






    def _reject_work(self):

        print "rejecting work on mturk"

    def _block_user(self):
        print "blocking worker on mturk"

    def _label_bad(self):
        print "labelling worker as bad in database"


    def _accept_work(self):
        print "accepting work here"



if __name__ == '__main__':
    test=Turk_Performance_Prototype(None,None)

    test.logic("joe","unknown",None,9999999999,True)





