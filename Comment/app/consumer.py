import pika
import requests
import json

import app.main as main
import app.schemas as schemas
import time


while True:
    try:
        params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.exchange_declare(exchange='user', exchange_type='fanout')
        channel.queue_declare(queue='user_comment', exclusive=True)
        channel.queue_bind(exchange='user', queue='user_comment')
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
        occupation = data['occupation'],
        avatar = data['avatar']
    )
    main.consumeUser(userInfo)

channel.basic_consume(queue='user_comment', on_message_callback=callback, auto_ack=True)

print("Comment consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
