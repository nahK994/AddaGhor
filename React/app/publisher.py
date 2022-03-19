import pika

def publish_message(post_id: str):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='react')
    channel.basic_publish(exchange='', routing_key='react', body=post_id)
    connection.close()