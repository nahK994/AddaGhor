import pika
import app.schemas as schemas
import json

def publish_message(user: schemas.UserModel):
    data = json.dumps(user.dict())
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='user', exchange_type='fanout')
    channel.basic_publish(exchange='user', routing_key='', body=data)
    connection.close()