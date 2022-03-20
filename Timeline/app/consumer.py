import pika
import requests
import json
import app.main as main
import app.schemas as schemas


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_timeline')
channel.queue_declare(queue='react_timeline')

def post_callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create post timeline ==> ", data)
    postInfo = schemas.PostModel(
        userId = data['userId'],
        postText = data['postText'],
        postDateTime = data['postDateTime'],
        postId = data['postId']
    )
    main.consumePost(postInfo)

def react_callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("update react timeline ==> ", data)
    reactInfo = schemas.ReactModel(
        postId = data['postId'],
        reactId = data['reactId'],
        smileReactCount = data['smileReactCount'],
        loveReactCount = data['loveReactCount'],
        likeReactCount = data['likeReactCount']
    )

    main.consumeReactsForPost(reactInfo)

channel.basic_consume(queue='post_timeline', on_message_callback=post_callback, auto_ack=True)
channel.basic_consume(queue='react_timeline', on_message_callback=react_callback, auto_ack=True)

print("Timeline consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
