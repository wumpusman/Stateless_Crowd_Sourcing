from enum import Enum
import manage_hits
from python_query_aws.env_info import Environment_Info
import boto3
import os



class task_result_parameters(Enum):
    Assignments="Assignments"

    Worker_ID="WorkerId"
    SubmitTime="SubmitTime"
    Assignment_ID="AssignmentId"

def get_active_users_in_latest_task(my_recent_task=0,endpoint_type="live"):
    session = boto3.Session(profile_name=None)
    keys = Environment_Info.static_get_special_code()
    endpoint_type = endpoint_type


    client = session.client(
        service_name='mturk',
        region_name='us-east-1',
        endpoint_url=Environment_Info.environments[endpoint_type]['endpoint'],
        aws_access_key_id=keys["aws_access_key_id"],
        aws_secret_access_key=keys["aws_secret_access_key"]
    )


    response = client.list_hits( #get the latest hit
         MaxResults=my_recent_task+1)

    latestTask=response["HITs"][my_recent_task]['HITId']

    results= Environment_Info.request_hit_results(client,hit_id=latestTask,hit_types=["Submitted"],max_return=999)


    return results


if __name__ == '__main__':
    vals=get_active_users_in_latest_task(0)
    print vals.keys()
    print vals["Assignments"][0].keys()