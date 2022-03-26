import pika
import requests
import json

import app.main as main
import app.schemas as schemas
import time


while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='user_comment')
        print("comment consumer online")
        break
    except:
        print("comment consumer failed")
        time.sleep(3)


def callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("Update user_name ==> ", data)
    userInfo = schemas.UserModel(
        userId = data['userId'],
        userName = data['userName'],
        email = data['email'],
        bio = data['bio'],
        password = data['password'],
        occupation = data['occupation']
    )
    main.updateUserInfo(userInfo)

channel.basic_consume(queue='user_comment', on_message_callback=callback, auto_ack=True)

print("Comment consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
