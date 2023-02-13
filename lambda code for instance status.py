import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):

    client = boto3.client('ec2')

    # Get the current time
    now = datetime.now()

    # Get a list of all running instances
    instances = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    msg = ''
    # Loop through the instances
    long_running_instances = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            # Calculate the instance launch time
            launch_time = instance['LaunchTime'].replace(tzinfo=None)
            launch_time_delta = now - launch_time

            # Check if the instance has been running for more than 2 days
            if launch_time_delta > timedelta(days=2):
                long_running_instances.append(instance)
                print(f"The following instances have been running for more than 2 days")
                ltime = str(launch_time)
                message = "Instance ID: "+instance['InstanceId']+" Launch time:" +ltime+"\n"
                print(message)
                msg = msg + message

    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:658907380213:scc-hpc-python101-topicrajesh',
        Message=msg,
        Subject='The following instance have been running for more than 2 days'
    )


    print(msg)