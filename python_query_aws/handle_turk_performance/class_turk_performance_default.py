from python_query_aws.handle_turk_performance.class_turk_performance_prototype import Turk_Performance_Prototype


class Turk_Performance_Default(Turk_Performance_Prototype):

    def __init__(self,client,session,maximum_time,msg_for_bad_performance, parameters_bad_performance={},parameters_acceptable_performance={}):
        super(Turk_Performance_Default, self).__init__(client,session)

        self.set_default_actions(parameters_bad_performance,parameters_acceptable_performance) #override with the current ones

        self.msg_for_rejection=msg_for_bad_performance
        self.threshold_for_completion=maximum_time

        self._FINISHED_SWITCH=False #If I'm done, this thing should not be called again



    def set_default_actions(self,parameters_bad,parameters_good):
        super(Turk_Performance_Default,self).set_default_actions(parameters_bad,parameters_good)

        for func_dict in self.actions_to_take_for_disqualification:
            func_dict["parameters"]=parameters_bad

        for func_dict in self.actions_to_take_for_qualification:
            func_dict["parameters"] = parameters_good

    def _accept_work(self,assignment_id):
        #lf.cse
        self._update_mturk_account(assignment_id,True)


    def logic(self,user_name,user_state, relative_time, user_exists):
        if self._FINISHED_SWITCH==True:
            warning="logic for user {} for assignment  was already called for this object, meant to be called once".format(user_name)
            raise Exception(warning)
        super(Turk_Performance_Default, self).logic(user_state, relative_time, user_exists)
        self._FINISHED_SWITCH=True #never call it twice



if __name__ == '__main__':
   temp= Turk_Performance_Default(None,None)
   temp.logic("joe","unknown",None,9999999999,True)
