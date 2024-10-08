import pika
from user.models import UserProfile
from timeline.models import Comment, Post, React
import json


def initiate_channel():
    params = pika.URLParameters('amqps://yzmvpdbx:9lISIr_7LPy-RPUFOa_BNUhW9oNeyeNy@shrimp.rmq.cloudamqp.com/yzmvpdbx')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return channel


class ActionType:
    post = "POST"
    delete = "DELETE"
    put = "PUT"


def publish_user(action_type: ActionType, user_profile_info: UserProfile):
    if action_type == ActionType.post or action_type == ActionType.put:
        data = {
            'actionType': action_type,
            'id': user_profile_info.user.id,
            'userProfileId': user_profile_info.id,
            'email': user_profile_info.user.email,
            'name' : user_profile_info.user.name,
            'bio'  : user_profile_info.bio,
            'profilePicture': 'google.com'
        }
    else:
        data = {
            'actionType': action_type,
            'id': user_profile_info.user.id
        }
    data = json.dumps(data)
    while True:
        try:
            channel = initiate_channel()
            channel.basic_publish(exchange='exchange', routing_key='user', body=data)
            break
        except Exception as e:
            print(str(e))
    

def publish_post(action_type: ActionType, post_info: Post):
    if action_type == ActionType.post or action_type == ActionType.put:
        data = {
            "actionType": action_type,
            "id": post_info.id,
            "user": post_info.user.id,
            "text": post_info.text
        }
    else:
        data = {
            "id": post_info.id,
            "actionType": ActionType.delete
        }
    data = json.dumps(data)
    while True:
        try:
            channel = initiate_channel()
            channel.basic_publish(exchange='exchange', routing_key='post', body=data)
            break
        except Exception as e:
            print(str(e))


def publish_comment(action_type: ActionType, comment_info: Comment):
    if action_type == ActionType.post or action_type == ActionType.put:
        data = {
            "actionType": action_type,
            "id": comment_info.id,
            "user": comment_info.user.id,
            "text": comment_info.text,
            "post": comment_info.post.id
        }
    else:
        data = {
            "id": comment_info.id,
            "actionType": ActionType.delete
        }
    data = json.dumps(data)
    while True:
        try:
            channel = initiate_channel()
            channel.basic_publish(exchange='exchange', routing_key='comment', body=data)
            break
        except Exception as e:
            print(str(e))


def publish_react(action_type: ActionType, react_info: React):
    if action_type == ActionType.post or action_type == ActionType.put:
        data = {
            "actionType": action_type,
            "id": react_info.id,
            "user": react_info.user.id,
            "type": react_info.type,
            "post": react_info.post.id
        }
    else:
        data = {
            "id": react_info.id,
            "actionType": ActionType.delete
        }
    data = json.dumps(data)
    while True:
        try:
            channel = initiate_channel()
            channel.basic_publish(exchange='exchange', routing_key='react', body=data)
            break
        except Exception as e:
            print(str(e))
