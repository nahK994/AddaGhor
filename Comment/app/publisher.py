import pika
import app.schemas as schemas
import json

def publish_message(comment: schemas.CommentModel):
    data = json.dumps(comment.dict())
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='comment_timeline')
    channel.basic_publish(exchange='', routing_key='comment_timeline', body=data)
    connection.close()