import pika
from . import schemas
import json

def publish_message(post: schemas.PostModel):
    data = json.dumps(post.dict())
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='post_react')
    channel.basic_publish(exchange='', routing_key='post_react', body=data)

    channel.queue_declare(queue='post_timeline')
    channel.basic_publish(exchange='', routing_key='post_timeline', body=data)
    connection.close()