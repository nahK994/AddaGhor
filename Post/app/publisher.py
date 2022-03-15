import pika

def publish_message(post_id: str):
    # channel = initiate_rabbitmq_channel()
    print("HaHa 1 post_id = ", post_id)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    print("HaHa 2")
    channel.queue_declare(queue='hello')
    print("HaHa 3")
    channel.basic_publish(exchange='', routing_key='hello', body=post_id)
    print("HaHa 4")
    connection.close()
    print("HaHa 5")