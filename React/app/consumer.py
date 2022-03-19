import pika
import requests
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_react')

def callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create react ==> ", data)
    url = 'http://localhost:8002/react/create/' + str(data['postId'])
    requests.post(url = url)

channel.basic_consume(queue='post_react', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
