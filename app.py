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




conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test") #temp2
#meta.drop_all(bind=conn)  # clear everything
#Base.metadata.create_all(conn)
manager = Manager(session,max_time=7) #in minutes

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")




@app.route('/api/get_results',methods=["POST"])
def dashboard():
    '''


    :return:
    '''
    userData = request.form['jsonData']
    userData = json.loads(userData)

    results= manager.prepare_results(userData["id"])
    return json.dumps({"results":results})


@app.route('/api/disconnect',methods=['POST'])
def disconnect():
    userData = request.form['jsonData'];
    userData = json.loads(userData)
    user = manager.select_user(userData["name"], userData["password"])
    if user!= None:
        if len(user.associated_content) > 0:
            assigned_content = user.get_current_content_in_progress(session)
            if assigned_content != None:
                manager.unassign_content(assigned_content)
            #this is used to handle users who are either refreshing the page , or exiting without finishing


    return json.dumps({"refresh":True})

@app.route('/api/submit',methods=['POST'])
def submit():
    userData = request.form['jsonData'];
    userData = json.loads(userData)
    name=userData['name']
    password=userData['password']
    result=userData["results"]
    session_expired=False


    if "session_expired" in userData:
        session_expired = userData["session_expired"]
        print "IS THIS CALLED"

    user = manager.select_user(userData["name"], userData["password"])




    if user==None: return json.dumps(manager.prepare_view(None))

    manager.update_global_state(user, {"value": result}) #This is where the magic happens

    assigned_content=None
    if session_expired == False:

        work_in_progress=user.get_current_content_in_progress(session)

        if type(work_in_progress)!=type(None):
            assigned_content = work_in_progress
            #such bad practice, add date for when this piece is going to be worked on
            assigned_content.assigned_date = datetime.datetime.now()

            session.add(assigned_content)
            session.commit()

            print "WHATS GOING ON"
            print assigned_content
            print assigned_content.assigned_date
        else:
            assigned_content = manager.assign_new_content(user)


        new_view = manager.prepare_view(assigned_content)  # update the view
        return json.dumps({"task": new_view})

    else:
        return json.dumps({"task":manager.prepare_view(None)})





@app.route('/api/login',methods=['POST'])
def login(): #For logging in
    userData = request.form['jsonData'];
    userData = json.loads(userData)

    if manager.does_user_exist(userData["name"])==False:
        manager.create_user(userData["name"],userData["password"])
        user = manager.select_user(userData["name"], userData["password"])

        manager.assign_new_content(user)


    user=manager.select_user(userData["name"], userData["password"])

    print "WTF"
    print session.query(Content).filter(Content.user_id==user.name).all()

    #No password
    if user == None:
        response = {
            'task': 'failure'
        }
        return json.dumps(response)

    new_content=None

    if len(user.associated_content)==0:
        new_content= manager.assign_new_content(user)
    else:
        new_content= user.get_current_content_in_progress(session)
        #reset the time, since they are coming back to it, this should be changed though
        new_content.assigned_date=datetime.datetime.now()
        session.add(new_content)
        session.commit()
    #htis is redundnant
    if len(user.associated_content)==0:
        return json.dumps({"task":manager.prepare_view(None)})

    return json.dumps({"task":manager.prepare_view(new_content)})








if __name__ == '__main__':

    #run_example.setup_example(session)
    app.run()