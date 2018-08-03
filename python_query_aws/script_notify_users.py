
from python_query_aws.env_info import Environment_Info
import boto3
import os
import datetime

if __name__ == '__main__':
    #PARAMETERS
    session = boto3.Session(profile_name=None)
    keys = Environment_Info.static_get_special_code()
    endpoint_type="live"

    file_name="user_qualification_groups/acceptable_users"
    max_time_before_warning_in_seconds=180 #must call this function 3 minutes after creating a mturk experiment

    #####Function
    list_of_workers = []
    with open(file_name, "rb") as f:
        list_of_workers = f.read().split("\n")

    list_of_list_workers=[]

    #quick way of going through to ensure sending messages is below 100 max
    if len(list_of_workers)>99:
        current_list=[]
        for num in xrange(len(list_of_workers)):
            if len(current_list)==99:
                list_of_list_workers.append(current_list)


            current_list.append(list_of_workers[num]) #split up list of workers into 2d array - i should have used numpy
    else:
        list_of_list_workers.append(list_of_workers)


    client = session.client(
        service_name='mturk',
        region_name='us-east-1',
        endpoint_url=Environment_Info.environments[endpoint_type]['endpoint'],
        aws_access_key_id=keys["aws_access_key_id"],
        aws_secret_access_key=keys["aws_secret_access_key"]
    )

    response = client.list_hits( #get the latest hit
     MaxResults=1)



    latestTask=response["HITs"][0]['HITTypeId']

    creationTime=response["HITs"][0]["CreationTime"]

    currentTime=datetime.datetime.now()
    currentTime=currentTime.replace(tzinfo=creationTime.tzinfo)

    diff_in_seconds=currentTime-creationTime
    diff_in_seconds=diff_in_seconds.total_seconds()

    if diff_in_seconds> max_time_before_warning_in_seconds:
        warning_format="minimum time of {} exceeded after creation of mturk task, currently at {} seconds".format(max_time_before_warning_in_seconds,diff_in_seconds)
        raise  Exception(warning_format)

    task_link= Environment_Info.environments[endpoint_type]['preview'] + "?groupId={}".format(latestTask)
    #print task_link
    #raw_input("WAIT")

    sbj_header = "Request to do additional HIT related to ongoing experiment - {}".format(task_link)
    msg= " I've linked the HIT to do below.\n - Should take as before around 6-7 minutes, although due to previous requests, I've extended the submission time just in case. \n {} \n If you have any questions, I'm happy to answer them \n - Regards Mike (SI lab) .".format(task_link)

    print msg
    for worker_id_arry in list_of_list_workers:
        for worker_id in worker_id_arry:
            try:
                client.notify_workers(Subject=sbj_header,
                                      MessageText=msg,
                                      WorkerIds=[worker_id])
            except:
                print "{} failure in script_notify_users to notify".format(worker_id)


