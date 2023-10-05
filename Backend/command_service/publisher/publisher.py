import pika
from user.models import UserProfile
from timeline.models import Comment, Post
import json


params = pika.URLParameters('amqps://itqdjkpt:6GAMl22_0xjDtFVbmslqDEZ-mtqN7VqP@shrimp.rmq.cloudamqp.com/itqdjkpt')
connection = pika.BlockingConnection(params)
channel = connection.channel()


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
            'profilePicture': 'google.com',
            'password': user_profile_info.user.password
        }
    else:
        data = {
            'actionType': action_type,
            'id': user_profile_info.user.id
        }
    data = json.dumps(data)
    channel.basic_publish(exchange='exchange', routing_key='user', body=data)
    

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
    channel.basic_publish(exchange='exchange', routing_key='post', body=data)


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
    channel.basic_publish(exchange='exchange', routing_key='comment', body=data)
