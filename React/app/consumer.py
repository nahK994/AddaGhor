import pika
import requests
import json

import app.main as main

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_react')

def initiateReactsForPost(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create react ==> ", data)
    main.initiateReactsForPost(data['postId'])

channel.basic_consume(queue='post_react', on_message_callback=initiateReactsForPost, auto_ack=True)

print("React consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
