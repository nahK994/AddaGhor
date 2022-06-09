import pika
import app.schemas as schemas
# import schemas
import json

def publish_message(react: schemas.ReactModel):
    data = json.dumps(react.dict())
    params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='react_timeline')
    channel.basic_publish(exchange='', routing_key='react_timeline', body=data)
    connection.close()