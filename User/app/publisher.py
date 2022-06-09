import pika
import app.schemas as schemas
import json

def publish_message(user: schemas.UserModel):
    data = json.dumps(user.dict())
    params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='user', exchange_type='fanout')
    channel.basic_publish(exchange='user', routing_key='', body=data)
    connection.close()