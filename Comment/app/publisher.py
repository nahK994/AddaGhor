import pika
import app.schemas as schemas
import json

def publish_message(comment: schemas.CommentModel):
    data = json.dumps(comment.dict())

    params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='comment_timeline')
    channel.basic_publish(exchange='', routing_key='comment_timeline', body=data)
    connection.close()