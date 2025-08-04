import boto3

ec2Client = boto3.client('ec2')

resp = ec2Client.describe_security_groups()

sec_groups= set()
for groups in resp["SecurityGroups"]:
 #   print(groups["GroupId"])
    for rules in groups["IpPermissions"]:
        for ips in rules["IpRanges"]:
            if ips["CidrIp"] == "0.0.0.0/0":
                sec_groups.add(groups["GroupId"])
#print("Final")
#print(list(sec_groups))

describe_vm = ec2Client.describe_instances(
    Filters=[
        {
            'Name': 'instance.group-id',
            'Values': list(sec_groups)
        }
    ]
)
for Reservation in describe_vm['Reservations']:
        for Instance in Reservation['Instances']:
            print(Instance["InstanceId"])
