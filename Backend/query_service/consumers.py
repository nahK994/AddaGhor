import pika
import json
from eventHandlers.userEventHandlers import *
from eventHandlers.postEventHandlers import *
from eventHandlers.commentEventHandlers import *


class ActionType:
    post = "POST"
    delete = "DELETE"
    put = "PUT"


def userInfoCallback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("user ==> ", data)
    action_type = data['actionType']
    if action_type == ActionType.post:
        userCreateEventHandler(data)
    elif action_type == ActionType.put:
        userUpdateEventHandler(data)
    else:
        userDeleteEventHandler(data)


def postInfoCallback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("post ==> ", data)
    action_type = data['actionType']
    if action_type == ActionType.post:
        postCreateEventHandler(data)
    elif action_type == ActionType.put:
        postUpdateEventHandler(data)
    else:
        postDeleteEventHandler(data)


def commentInfoCallback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("comment ==> ", data)
    action_type = data['actionType']
    if action_type == ActionType.post:
        commentCreateEventHandler(data)
    elif action_type == ActionType.put:
        commentUpdateEventHandler(data)
    else:
        commentDeleteEventHandler(data)


params = pika.URLParameters('amqps://itqdjkpt:6GAMl22_0xjDtFVbmslqDEZ-mtqN7VqP@shrimp.rmq.cloudamqp.com/itqdjkpt')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='exchange', exchange_type='topic')

queue1 = channel.queue_declare('', exclusive=True)
queue_name1 = queue1.method.queue
channel.queue_bind(exchange='exchange', queue=queue_name1, routing_key='user')

queue2 = channel.queue_declare('', exclusive=True)
queue_name2 = queue2.method.queue
channel.queue_bind(exchange='exchange', queue=queue_name2, routing_key='post')

queue3 = channel.queue_declare('', exclusive=True)
queue_name3 = queue3.method.queue
channel.queue_bind(exchange='exchange', queue=queue_name3, routing_key='comment')



channel.basic_consume(queue=queue_name1, on_message_callback=userInfoCallback, auto_ack=True)
channel.basic_consume(queue=queue_name2, on_message_callback=postInfoCallback, auto_ack=True)
channel.basic_consume(queue=queue_name3, on_message_callback=commentInfoCallback, auto_ack=True)

print("consumer online")
channel.start_consuming()
