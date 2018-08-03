from python_query_aws import script_current_task_results
from python_query_aws import script_turk_performance
from sqlalchemy import desc
from backend import db_connection2 as db
from class_turk_performance_default import Turk_Performance_Default
from python_query_aws.env_info import Environment_Info
import boto3

db_name = "Task_Crowd_Source_Test"


conn, meta, session = db.connect("postgres", "1234", db=db_name)

keys = Environment_Info.static_get_special_code()
endpoint_type = "live"
client_session_turk = boto3.Session(profile_name=None)

client = client_session_turk.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=Environment_Info.environments[endpoint_type]['endpoint'],
    aws_access_key_id=keys["aws_access_key_id"],
    aws_secret_access_key=keys["aws_secret_access_key"]
)

results = script_current_task_results.get_active_users_in_latest_task(0, endpoint_type)

recent_performance= script_turk_performance.get_recently_submitted_results(session, results, max_results=2, time_offset=14395.592572)


name=recent_performance[0]["user"]
user_exists=recent_performance[0]["user_exists"]
user_quality=recent_performance[0]["user_quality"]
assignment_id=recent_performance[0]["assignment_id"]
relative_time=-1#failed
if user_exists != False:
    if len(recent_performance[0]["results"])!=0:

        relative_time=float(recent_performance[0]["results"][0]['relative_time'])
    else:
        user_exists=False #User did nothing, they are as good as dead to me

one_user=Turk_Performance_Default(client,session,1200,msg_for_bad_performance="",parameters_acceptable_performance={"assignment_id":assignment_id})



one_user.logic(user_name=name,user_state=user_quality,relative_time=relative_time,user_exists=user_exists
               )

print name
print relative_time
print user_exists
print one_user.should_disqualify_user(user_quality,relative_time,user_exists)