import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings_local")
django.setup()


import pika
import time
import json
from user.userEventHandlers import userCreateEventHandler, userUpdateEventHandler, userDeleteEventHandler


class ActionType:
    post = "POST"
    delete = "DELETE"
    put = "PUT"


while True:
    try:
        params = pika.URLParameters(
            'amqps://itqdjkpt:6GAMl22_0xjDtFVbmslqDEZ-mtqN7VqP@shrimp.rmq.cloudamqp.com/itqdjkpt')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.exchange_declare(exchange='user', exchange_type='fanout')
        channel.queue_declare(queue='user', exclusive=True)
        channel.queue_bind(exchange='user', queue='user')
        print("user consumer online")

        # channel.exchange_declare(exchange='question', exchange_type='fanout')
        # channel.queue_declare(queue='result_question', exclusive=True)
        # channel.queue_bind(exchange='question', queue='result_question')
        # print("result question consumer online")

        # channel.exchange_declare(exchange='topic', exchange_type='fanout')
        # channel.queue_declare(queue='result_topic', exclusive=True)
        # channel.queue_bind(exchange='topic', queue='result_topic')
        # print("result topic consumer online")

        # channel.exchange_declare(exchange='exam', exchange_type='fanout')
        # channel.queue_declare(queue='result_exam', exclusive=True)
        # channel.queue_bind(exchange='exam', queue='result_exam')
        # print("result exam consumer online")
        break
    except Exception as e:

        print(f"consumer failed +++> {str(e)}")
        time.sleep(3)


# from user.models import User, UserProfile


# def userCreateEventHandler(data):
#     user_obj = User.objects.create_user(data['name'], data['email'], data['password'])
#     UserProfile.objects.create(
#         user=user_obj,
#         bio=data['bio'],
#         profile_picture=data['profilePicture']
#     )

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


# def questionInfoCallback(ch, method, properties, body):
#     data = json.loads(body.decode('ASCII'))
#     print("question ==> ", data)
#     manageQuestionData(data)


# def topicInfoCallback(ch, method, properties, body):
#     data = json.loads(body.decode('ASCII'))
#     print("topic ==> ", data)
#     manageTopicData(data)


# def examInfoCallback(ch, method, properties, body):
#     data = json.loads(body.decode('ASCII'))
#     print("exam ==> ", data)
#     manageExamData(data)


channel.basic_consume(queue='user', on_message_callback=userInfoCallback, auto_ack=True)
# channel.basic_consume(queue='result_question', on_message_callback=questionInfoCallback, auto_ack=True)
# channel.basic_consume(queue='result_topic', on_message_callback=topicInfoCallback, auto_ack=True)
# channel.basic_consume(queue='result_exam', on_message_callback=examInfoCallback, auto_ack=True)

print("result consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()