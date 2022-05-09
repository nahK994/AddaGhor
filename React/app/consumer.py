import pika
import requests
import json

import app.main as main
import time

print("connecting....")
# # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.exchange_declare(exchange='post', exchange_type='fanout')
q = channel.queue_declare(queue='', exclusive=True)
post_react = q.method.queue
channel.queue_bind(exchange='post', queue=post_react)

print("react consumer online")

def initiateReactsForPost(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create react ==> ", data)
    main.initiateReactsForPost(data['postId'])

channel.basic_consume(queue=post_react, on_message_callback=initiateReactsForPost, auto_ack=True)

print("React consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
channel.close()