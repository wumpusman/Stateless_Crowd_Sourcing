from db_connection2 import *
class Manager:
    def __init__(self,session,max_time=7):
        self.session=session
        self._session_time=max_time*60



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
        if len(user.associated_content)>0:
            if user.associated_content[-1].is_completed==False:
                return Exception("assigning new content when current content is not complete")
        optional_content = user.get_content_where_user_was_uninvolved_and_is_not_part_of_rating_task(self.session).all()
        if len(optional_content)==0: return None
        chosen=optional_content[0]
        chosen.associated_user=user
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

        if(current.is_completed==True):
            return Exception("Content completed when it shouldn't be completed already")

        current.results= results["value"]
        current.is_completed=True

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