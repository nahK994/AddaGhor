import pika
import app.schemas as schemas
import json

def publish_message(react: schemas.ReactModel):
    data = json.dumps(react.dict())
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='react_timeline')
    channel.basic_publish(exchange='', routing_key='react_timeline', body=data)
    connection.close()