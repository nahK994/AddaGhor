import pika
import app.schemas as schemas
# import schemas
import json

def publish_message(post: schemas.PostModel):
    data = json.dumps(post.dict())
    print(data)
    # params = pika.URLParameters('localhost')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
    # connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='post', exchange_type='fanout')
    connection.close()