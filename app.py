import json
from random import randint

from flask import Flask, render_template
from flask import request

from backend import run_example
from backend.db_connection2 import *
from backend.manager import Manager

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")



manager =None


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/submit',methods=['POST'])
def submit():
    userData = request.form['jsonData'];
    userData = json.loads(userData)
    name=userData['name']
    password=userData['password']
    result=userData["results"]

    print "RESULTS ARE FOR SUBMIT"
    print result

    user = manager.select_user(userData["name"], userData["password"])

    assigned_content = user.associated_content[-1]
    if assigned_content != None:
        print assigned_content.origin_process
        print assigned_content.origin_process.id
        print assigned_content.origin_process.task_parameters_obj.body_of_task.id
        print assigned_content.origin_process.task_parameters_obj.body_of_task.results

    if user==None: return json.dumps({})

    manager.update_global_state(user,{"value":result})

    assigned_content= manager.assign_new_content(user)



    new_view=manager.prepare_view(assigned_content) #update the view
    return json.dumps({"task":new_view})


@app.route('/api/login',methods=['POST'])
def login(): #For logging in
    userData = request.form['jsonData'];
    userData = json.loads(userData)




    if manager.does_user_exist(userData["name"])==False:
        manager.create_user(userData["name"],userData["password"])
        user = manager.select_user(userData["name"], userData["password"])
        manager.assign_new_content(user)

    user=manager.select_user(userData["name"], userData["password"])
    #No password
    if user == None:
        response = {
            'task': 'failure'
        }
        return json.dumps(response)

    new_content=None
    if len(user.associated_content)==0:
        new_content= manager.assign_new_content(user)
    elif user.associated_content[-1].is_completed:
        new_content= manager.assign_new_content(user)
    else:
        new_content=user.associated_content[-1]


    #htis is redundnant
    if len(user.associated_content)==0:
        return json.dumps({"task":manager.prepare_view(None)})

    return json.dumps({"task":manager.prepare_view(new_content)})



    #Hand shake to db
    #  Provide a name, or use the following code, this will be linked to your results
    #   task that was just completed
    #
    '''
        Start Page - GenerateAlias Or Enter Name And Password

        OnKeyBoardPress Or switch button, send state

         State {
            Name
            Password
            Is_Finished
            Rating:
            Content:
         }

         Name Exists:
            If Does Not Exist - Create Account

        AssignContent
            Logic=Naive()
            UpdateLockedContent()

            Logic
                Update_User_Content_With_New_State_Information (Do Nothing If NO content)

                Check If Use Has Content:
                  If User_Is_Unfinished:
                    return User.Content
                Else:
                    return SelectNewContent()

            SelectNewContent()


        UpdateLockedContent():
            For AllContent That IsUnlocked, And Is Chosen
                If AllContent.Children that are not rating are Chosen, Lock this


            Select AllContent That Is not locked and Is_Finished nad is_chosen and type is not Rating
                For Each Content in AllContent.Children - The Possible Inhereitators
                    If Content isRating Locked It Ratings can't have children
                    Else
                        DetermineLock - Naive, if it's been scored 3 times, then it cannot be used
                            If Content Is Not Locked
                                    If Content Select Ratings > 3
                                        Lock It

        Project1Logic Extends Naive






    '''
    #On Key entered - update information
    #Take random token name Or Provide

    response = {
        'randomNumber': randint(1, 100)
    }
    return json.dumps(response)

if __name__ == '__main__':
    conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test")
    meta.drop_all(bind=conn)  # clear everything
    Base.metadata.create_all(conn)
    manager = Manager(session)
    run_example.setup_example(session)
    app.run()