import boto3
import sys


resource = sys.argv[1] # ec2 , vpc

aws_access_key = "##############"
aws_secret_key = "###########"
aws_region = "ap-south-1"

def vpc_details(client):
  #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpcs.html
  vpc_info = client.describe_vpcs()
  vpc_list=[]
  for vpcs in vpc_info["Vpcs"]:
    result = {}
    vpc_id = vpcs["VpcId"]
    for tags in vpcs["Tags"]:
      if tags["Key"] == 'Name':
        vpc_name = tags["Value"]
    subnets_list=[]
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_subnets.html
    subnet_details = client.describe_subnets(
      Filters=[
        {
          'Name': 'vpc-id', 
          'Values': [vpc_id] 
         }
      ]
    )
    sub_dict={}
    for subnets in subnet_details["Subnets"]:
      sub_dict = {
        "subnetId": subnets['SubnetId'],
        "CidrBlock":subnets['CidrBlock'],
        "AvailabilityZone": subnets['AvailabilityZone']
      }
      subnets_list.append(sub_dict)
    result = {
    "vpcName": vpc_name,
    "vpcId": vpc_id,
    "vpcCidr": vpcs["CidrBlock"],
    "region": aws_region,
    "Subnets": subnets_list
    }
    vpc_list.append(result)
  return vpc_list 

def vm_details(client):
  result=[]
  describe_vm = client.describe_instances()
  for items in describe_vm["Reservations"]:
    instance_dict={}
    for instance in items["Instances"]:
      for tags in instance["Tags"]:
        if tags["Key"] == 'Name':
            instance_name = tags["Value"]
      if instance["State"]["Name"] == "terminated":
        publicAdress = "null"
        privateAddress = "null"
        vpcid = "null"
        subnetid = "null"
      else:
        publicAdress = instance["PublicIpAddress"]
        privateAddress = instance["PrivateIpAddress"]
        vpcid = instance["VpcId"]
        subnetid = instance["SubnetId"]

      instance_dict={
        "instanceName" : instance_name,
        "instanceId" : instance["InstanceId"],
        "ImageId" : instance["ImageId"],
        "InstanceType": instance["InstanceType"],
        "InstanceState": instance["State"]["Name"],
        "PrivateIpAddress" : privateAddress,
        "PublicIpAddress" : publicAdress,
        "VpcId": vpcid,
        "SubnetId": subnetid,
        "AvailabilityZone": instance["Placement"]["AvailabilityZone"]
      }
    result.append(instance_dict)
  return result

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
ec2Client = boto3.client('ec2',
              aws_access_key_id=aws_access_key,
              aws_secret_access_key=aws_secret_key,
              region_name=aws_region)

if resource.lower() == 'ec2':
  print("EC2")
  print(vm_details(ec2Client))
elif resource.lower() == 'vpc':
  print(vpc_details(ec2Client))
else:
  print("please provide value ec2 or vpc as command line argument!")
  exit