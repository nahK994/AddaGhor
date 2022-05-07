import pika
import requests
import json

# import main
import app.main as main
import time

# amqp://guest:guest@localhost:5672
while True:
    try:
        print("connecting....")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        channel = connection.channel()
        channel.exchange_declare(exchange='post', exchange_type='fanout')
        channel.queue_declare(queue='post_react', exclusive=True)
        channel.queue_bind(exchange='post', queue='post_react')

        print("react consumer online")
        break
    except:
        print("react consumer failed")
        time.sleep(3)

# params = pika.URLParameters('amqps://eykbbnzj:nytVuZcErKh3WFkY5DawOnZGKrHl9fF4@shrimp.rmq.cloudamqp.com/eykbbnzj')
# connection = pika.BlockingConnection(params)
# params = pika.URLParameters('localhost')


# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel = connection.channel()
# channel.exchange_declare(exchange='post', exchange_type='fanout')
# channel.queue_declare(queue='post_react', exclusive=True)
# channel.queue_bind(exchange='post', queue='post_react')

# print("react consumer online")

def initiateReactsForPost(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create react ==> ", data)
    main.initiateReactsForPost(data['postId'])

channel.basic_consume(queue='post_react', on_message_callback=initiateReactsForPost, auto_ack=True)

print("React consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
channel.close()