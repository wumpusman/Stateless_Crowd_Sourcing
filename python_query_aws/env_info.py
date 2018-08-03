import datetime
import os
class Environment_Info(object):
    create_hits_in_live = False

    environments = {
        "live": {
            "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
            "preview": "https://www.mturk.com/mturk/preview",
            "manage": "https://requester.mturk.com/mturk/manageHITs",
            "reward": "0.00"
        },
        "sandbox": {
            "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
            "preview": "https://workersandbox.mturk.com/mturk/preview",
            "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
            "reward": "0.11"
        },
    }

    @staticmethod
    def query_sandbox():
       return  Environment_Info.environments["sandbox"]

    @staticmethod
    def static_get_special_code():
        '''
        This shoudl be removed
        '''
        #print os.environ.get("AWS_SECRET_ACCESS_KEY")
        #print os.environ.get("AWS_ACCESS_KEY_ID")
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key =  os.environ.get("AWS_SECRET_ACCESS_KEY")

        return {"aws_access_key_id":aws_access_key_id,
                "aws_secret_access_key":aws_secret_access_key}


    @staticmethod
    def get_test_requirements():
        # Example of using qualification to restrict responses to Workers who have had
        # at least 80% of their assignments approved. See:
        # http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs
        worker_requirements = [{
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [0],
            'RequiredToPreview': True,
        }]

        return worker_requirements

    @staticmethod
    def get_test_task_layout():
        question_sample = open("my_question.xml", "r").read()
        return question_sample

    @staticmethod
    def request_hit_results(client, hit_id,hit_types=['Submitted'], max_return=100):
        '''

        :param client:
        :param hit_id:
        :param hit_types: Array of optional types - see mturk API for types
        :param max_return:
        :return:
        '''
        response = client.list_assignments_for_hit(
            HITId=hit_id,
            AssignmentStatuses=hit_types,
            MaxResults=10,
        )
        return response

    @staticmethod
    def make_hit(client,title,task_layout,requirements,max_assignments, duration,lifetime_duration
                 ,keywords="",description="",   reward="0.00"):
    # Create the HIT
        response = client.create_hit(
            MaxAssignments=3,
            LifetimeInSeconds=600,
            AssignmentDurationInSeconds=600,
            Reward=reward,
            Title=title,
            Keywords=keywords,
            Description=description,
            Question=task_layout,
            QualificationRequirements=requirements,
        )
        return response

    @staticmethod
    def delete_hit_quick(client, hit_id):
        response2 = client.update_expiration_for_hit(
            HITId=hit_id,
            ExpireAt=datetime.datetime(2000, 1, 1)
        )

        response = client.delete_hit(
            HITId=hit_id
        )


    @staticmethod
    def make_test_hit(client,title='The end is neigh2',task_layout=None,
                      requirements=None,max_assignments=3,duration=600,lifetime_duration=9000,
                      keywords='question, answer, research',
                      description='Answer a simple question. Created from mturk-code-samples.',
                      reward="0.11"):

        task_layout=Environment_Info.get_test_task_layout()
        requirements=Environment_Info.get_test_requirements()

        return Environment_Info.make_hit(client,title,task_layout,
                                         requirements,max_assignments,
                                         duration,lifetime_duration,keywords,description,reward)


    @staticmethod
    def static_assign_qualification_to_workers(client,list_of_worker_ids,qualification_id,assigned_value):
            for worker_id in list_of_worker_ids:
                try:
                    client.associate_qualification_with_worker(
                        QualificationTypeId=qualification_id,
                        WorkerId=worker_id,
                        IntegerValue=assigned_value,
                        SendNotification=False


                    )
                except:
                    print "{} worker failed at static_assign_qualificaiton_to_workers".format(worker_id)
