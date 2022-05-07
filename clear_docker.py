import os

def delete_image(image_name):
    return f"gnome-terminal -e 'bash -c \"docker image rm -f {image_name}; bash\" '" 

def delete_container(container_name):
    return f"gnome-terminal -e 'bash -c \"docker container rm -f {container_name}; bash\" '" 

os.system(delete_container('addaghor_react_1'))
os.system(delete_container('addaghor_post_1'))
os.system(delete_container('addaghor_consumer_1'))
os.system(delete_container('addaghor_rabbitmq_1'))

os.system(delete_image('addaghor_react:latest'))
os.system(delete_image('addaghor_post:latest'))
os.system(delete_image('addaghor_consumer:latest'))