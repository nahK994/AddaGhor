import pika
from user import models
import json


class ActionType:
    post = "POST"
    delete = "DELETE"
    put = "PUT"


def publish_user(action_type: ActionType, user_profile_info: models.UserProfile):
    data = {}
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

    print("HIHI ===> ", data)
    data = json.dumps(data)
    params = pika.URLParameters('amqps://itqdjkpt:6GAMl22_0xjDtFVbmslqDEZ-mtqN7VqP@shrimp.rmq.cloudamqp.com/itqdjkpt')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='user', exchange_type='fanout')
    channel.basic_publish(exchange='user', routing_key='', body=data)
    connection.close()