import requests
from zipfile import ZipFile 
import os
import boto3


final="https://github.com/akhil-a/aws-cli-examples/archive/refs/heads/main.zip"
repo="akhil-a/aws-cli-examples"
branch="test_branch"
repo_name= repo.split("/")[-1].lower()
print(repo_name)
S3_BUCKET="mygithubrepo-bucket"

def download_code(repo, branch):
    repo_url=f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
    response=requests.get(repo_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download ZIP: {response.status_code}")
    return(response.content)

ec2Client = boto3.client('s3')
downloaded_file=download_code(repo,branch)
folder_name="/tmp"
zip_path=os.path.join(folder_name,f"{repo_name}.zip" )
print(zip_path)
if os.path.exists(folder_name):
    print("path exists")
else:
    os.makedirs(folder_name)
print(f"Downloading and saving {zip_path}")
with open(zip_path, mode="wb") as zip_file:
    zip_file.write(downloaded_file)
print("extracting")
with ZipFile(zip_path, mode="r") as toextract:
    toextract.extractall(folder_name) 
extracted_path=os.path.join(folder_name,f"{repo_name}-{branch}")
for (root,dirs,files) in os.walk(extracted_path, topdown=True):
    for file in files:
        path=os.path.join(root,file)
        relative_path=os.path.relpath(path,extracted_path)
        print(f"Uploading {relative_path}")
        s3_key =f"{repo_name}-{branch}/{relative_path}"
        ec2Client.upload_file(path, S3_BUCKET, s3_key)

