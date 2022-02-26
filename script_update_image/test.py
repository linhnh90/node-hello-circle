import docker

image = "130228678771.dkr.ecr.ap-southeast-1.amazonaws.com/python:34"
client = docker.from_env()
client.containers.run(image, ports={'5000/tcp': 5000}, name='python', detach=True)