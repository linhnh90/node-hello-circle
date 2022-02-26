from datetime import datetime
from email.mime import image
from http import client
from time import sleep
import boto3
import os
import docker
 
def write_log(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)


def print_time():   
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "Current Time = " + current_time
    return data

"""get latest tag images from ecr aws"""
def get_latest_image(name):
    client = boto3.client('ecr', region_name='ap-southeast-1')
    response = client.list_images(
        registryId='130228678771',
        repositoryName=name,
        maxResults=500
    )
    latest = None
    temp_tag = None

    for image in response['imageIds']:
        tag = image['imageTag']
        response = client.describe_images(
            registryId='130228678771',
            repositoryName='nodejs',
            imageIds=[
                {
                    'imageTag': tag
                }
            ]
        )
        push_at = response['imageDetails'][0]['imagePushedAt']
        if latest is None:
            latest = push_at
        else:
            if latest < push_at:
                latest = push_at
                temp_tag = tag
    return temp_tag, latest

def check_list_docker_running():
    cmd = "docker inspect --format='{{json .RepoTags }}' $(docker ps  | awk '{print $2}' | grep -v ID)"
    container_names = os.popen(cmd).read().split('\n')
    list_container = [ ]
    for i in container_names:
        if len(i) == 0:
            break
        else:
            container_name = i.split('"')[1].split('/')[1]
            list_container.append(container_name)
    return list_container

""" """
check_image = 'python'
version, push_at = get_latest_image(check_image)
print(f'app {check_image} {version} pushed at {push_at}')
list_image = check_list_docker_running()
print(list_image)
for i in list_image:
    if check_image in str(i).split(':'):
        if version != str(i).split(':')[1]:
            print("stop and remove", check_image)
            docker_stop = "docker container stop " + check_image + " && " + "docker container rm " + check_image
            os.system(docker_stop)
            client = docker.from_env()
            if check_image == "nodejs": 
                print("start nodejs", version)
                image = "130228678771.dkr.ecr.ap-southeast-1.amazonaws.com/nodejs:" + version
                client.containers.run(image, ports={'3000/tcp': 3000}, name='nodejs', detach=True)
                sleep(20)
            else:
                print("start python", version)
                image = "130228678771.dkr.ecr.ap-southeast-1.amazonaws.com/python:" + version
                client.containers.run(image, ports={'5000/tcp': 5000}, name='python', detach=True)
                sleep(20)
            data_log = "updated image " + check_image + " version " + version + " at " + print_time()
            write_log('nodejs_auto_update.log', data_log )

    else:
        data_log = "current image " + check_image + " is latest version " + version + " at " +print_time()
        write_log('nodejs_auto_update.log', data_log )

