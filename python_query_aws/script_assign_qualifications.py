
from mturk_samples.python_query_aws.env_info import Environment_Info
import boto3
import os


def assign_qualifications(user_type_file,score, endpoint_type="live",qualification_id="394TT8DUT87RHW5YRABW3893Z4OZTO"):
    session = boto3.Session(profile_name=None)
    keys = Environment_Info.static_get_special_code()

    endpoint_type = endpoint_type
    qualification_id = qualification_id
    file_name = os.path.join("user_qualification_groups", user_type_file)

    quality = -1

    list_of_workers = []
    with open(file_name, "rb") as f:
        list_of_workers = f.read().split("\n")

    client = session.client(
        service_name='mturk',
        region_name='us-east-1',
        endpoint_url=Environment_Info.environments[endpoint_type]['endpoint'],
        aws_access_key_id=keys["aws_access_key_id"],
        aws_secret_access_key=keys["aws_secret_access_key"]
    )

    list_of_workers = list_of_workers
    Environment_Info.static_assign_qualification_to_workers(
        client, list_of_workers, qualification_id, quality
    )


if __name__ == '__main__':
    assign_qualifications(user_type_file='bad_users',score=-1,endpoint_type='sandbox')