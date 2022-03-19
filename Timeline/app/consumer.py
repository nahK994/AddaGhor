import pika
import requests
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_timeline')

def post_callback(ch, method, properties, body):
    data = json.dumps(body.decode('ASCII'))
    print("create post timeline ==> ", data)
    url = 'http://localhost:8004/post/create/' + data
    requests.post(url = url)

channel.basic_consume(queue='post_timeline', on_message_callback=post_callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
