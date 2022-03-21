import pika
import app.schemas as schemas
import json

def publish_message(user: schemas.UserModel):
    data = json.dumps(user.dict())
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='user_post')
    channel.basic_publish(exchange='', routing_key='user_post', body=data)

    channel.queue_declare(queue='user_comment')
    channel.basic_publish(exchange='', routing_key='user_comment', body=data)

    channel.queue_declare(queue='user_timeline')
    channel.basic_publish(exchange='', routing_key='user_timeline', body=data)
    connection.close()