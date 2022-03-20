import pika
import requests
import json
import app.main as main
import app.schemas as schemas


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_timeline')

def post_callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create post timeline ==> ", data)
    main.initiateReactsForPost(data['postId'])
    postInfo = schemas.CreatePostModel(
        userId = data['userId'],
        postText = data['postText'],
        postDateTime = data['postDateTime']
    )
    main.initiatePost(postInfo)

channel.basic_consume(queue='post_timeline', on_message_callback=post_callback, auto_ack=True)

print("Timeline consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
