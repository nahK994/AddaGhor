import pika
from user import models
import json


class ActionType:
    post = "POST"
    delete = "DELETE"
    put = "PUT"


def publish_user(actionType: ActionType, userInfo: models.UserProfile):
    data = {}
    data['actionType'] = actionType
    data['id'] = userInfo.id
    if actionType == "POST" or actionType == "PUT":
        data['email'] = userInfo.user.email
        data['name'] = userInfo.user.name
        data['bio'] = userInfo.bio
        data['profile_picture'] = userInfo.profile_picture
        data['password'] = userInfo.user.password

    print("HIHI ===> ", data)
    data = json.dumps(data)
    params = pika.URLParameters('amqps://itqdjkpt:6GAMl22_0xjDtFVbmslqDEZ-mtqN7VqP@shrimp.rmq.cloudamqp.com/itqdjkpt')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='user', exchange_type='fanout')
    channel.basic_publish(exchange='user', routing_key='', body=data)
    connection.close()