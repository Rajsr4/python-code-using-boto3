import boto3
from prettytable import PrettyTable
ec2 = boto3.client('ec2')
cloudtrail = boto3.client('cloudtrail')
def get_user(instanceid):
        response = cloudtrail.lookup_events (
                LookupAttributes=[
                        {
                                'AttributeKey': 'ResourceName',
                                'AttributeValue': instanceid
                        }
                ],
        )
        return response
def get_ec2_owner(instanceid):
        user_details = get_user (instanceid)
        for event in user_details.get ("Events"):
                if event.get ("EventName") == "StartInstances":
                        return event.get ("Username")
                elif event.get ("EventName") == "RunInstances":
                        return event.get ("Username")
"""
response = ec2.describe_instances (Filters=[
        {
                'Name': 'instance-state-name',
                'Values': ['running']
        }
])
"""
response = ec2.describe_instances ()
table = PrettyTable()
table.field_names = ["Instance ID", "Username"]
for r in response['Reservations']:
        for instance in r['Instances']:
                user = get_ec2_owner (instance['InstanceId'])
                #print(user)
                if user == None:
                    ec2.create_tags(Resources=[instance['InstanceId']], Tags=[{"Key": "CreatedBy", "Value": "Unknown"}])
                    print("Added tag Unknown for instance : ",instance['InstanceId'])
                else :
                    ec2.create_tags(Resources=[instance['InstanceId']], Tags=[{"Key": "CreatedBy", "Value": user}])
                    print("Added tag "+str(user)+" for instance : "+str(instance['InstanceId']))
                #table.add_row([instance['InstanceId'],user])

print(table)
