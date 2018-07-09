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



#Task_Crowd_Source_Test
#conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test") #temp2
conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test") #temp2

#meta.drop_all(bind=conn)  # clear everything
#Base.metadata.create_all(conn)
manager = Manager(session,max_time=6) #in minutes
if type(os.environ.get('DATABASE_URL')) != type(None):
    manager._minimum_work_time=10
    manager._effort_ratio=1

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


def commit_close_session(session):
    import time
    time.sleep(.1)

    session.commit()
    session.close()
    pass

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

    #commit_close_session(session) #THIS IS FUCKING TERRIBLE PRACTICE :/
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


    user = manager.select_user(userData["name"], userData["password"])




    if user==None: return json.dumps(manager.prepare_view(None))
    if user.alias==Manager.user_bad:
        return json.dumps(manager.prepare_view(Manager.user_bad))
    did_they_do_it=manager.update_global_state(user, {"value": result}) #This is where the magic happens

    assigned_content=None
    if session_expired == False:

        work_in_progress=user.get_current_content_in_progress(session)

        if type(work_in_progress)!=type(None):
            assigned_content = work_in_progress
            #such bad practice, add date for when this piece is going to be worked on
            assigned_content.assigned_date = datetime.datetime.now()

            session.add(assigned_content)
            session.commit()

        else:
            assigned_content = manager.assign_new_content(user)


        new_view = manager.prepare_view(assigned_content)  # update the view
        return json.dumps({"task": new_view})

    else:
        return json.dumps({"task":manager.prepare_view(None)})


@app.route ('/api/edit',methods=['Post'])
def edit():
    userData = request.form['jsonData'];
    userData = json.loads(userData)
    print userData
    id=userData['content_id']
    p_id=userData['process_id']
    transformation_msg=userData['edit_type']
    result_value=userData["result"]
    #get associated content
    #get associated
    process_obj=session.query(Process_Object).filter(Process_Object.id==p_id).all()[0]
    content=session.query(Content).filter(Content.id==id).all()[0]
    result=False #if for some reason there is a mismatch

    if(content.origin_process_id==p_id):
        result=manager.edit_process(process_obj,content,transformation_msg,result_value)
    #session.query(Content).filter(Content.id==id).all()[0].originating_process_id
    #manager.edit_process(process,content,transformation_msg)
    return json.dumps({"results":result})


@app.route('/api/login',methods=['POST'])
def login(): #For logging in
    #poor taste

    #conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test")
    #manager.session=session

    userData = request.form['jsonData'];
    userData = json.loads(userData)

    if manager.does_user_exist(userData["name"])==False:

        manager.create_user(userData["name"],userData["password"])

        user = manager.select_user(userData["name"], userData["password"])

        manager.assign_new_content(user)


    user=manager.select_user(userData["name"], userData["password"])
    if manager.user_bad==user.alias:
        return json.dumps({"task": manager.prepare_view(manager.user_bad)}) #this means this user sucks

    print session.query(Content).filter(Content.user_id==user.name).all()

    #No password
    if user == None:
        response = {
            'task': 'failure'
        }
        return json.dumps(response)

    new_content=None


    if (user.get_current_content_in_progress(session))==None:
        new_content= manager.assign_new_content(user)
    else:
        print "HERE THOUGH?"
        new_content= user.get_current_content_in_progress(session)
        #reset the time, since they are coming back to it, this should be changed though
        new_content.assigned_date=datetime.datetime.now()
        session.add(new_content)
        session.commit()

    #htis is redundnant
    print "did i make ith ere htouhg?"

    if len(user.associated_content)==0:
        return json.dumps({"task":manager.prepare_view(None)})
    print "MADE I HERE????"
    return json.dumps({"task":manager.prepare_view(new_content)})








if __name__ == '__main__':

    #run_example.setup_example(session)
    app.run()