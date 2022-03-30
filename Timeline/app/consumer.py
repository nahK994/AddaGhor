import pika
import requests
import json
import app.main as main
import app.schemas as schemas
import time


while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='user', exchange_type='fanout')
        channel.queue_declare(queue='user_timeline', exclusive=True)
        channel.queue_bind(exchange='user', queue='user_timeline')

        channel.exchange_declare(exchange='post', exchange_type='fanout')
        channel.queue_declare(queue='post_timeline', exclusive=True)
        channel.queue_bind(exchange='post', queue='post_timeline')

        channel.queue_declare(queue='react_timeline')
        channel.queue_declare(queue='comment_timeline')
        print("timeline consumer online")
        break
    except:
        print("timeline consumer failed")
        time.sleep(3)


def post_callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("create post timeline ==> ", data)
    postInfo = schemas.PostModel(
        userId = data['userId'],
        userName = data['userName'],
        postId = data['postId'],
        postText = data['postText'],
        postDateTime = data['postDateTime'],
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

def comment_callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("update comment timeline ==> ", data)
    commentInfo = schemas.CommentModel(
        commentText = data['commentText'],
        commentDateTime = data['commentDateTime'],
        postId = data['postId'],
        userId = data['userId'],
        userName = data['userName'],
        commentId = data['commentId']
    )
    main.consumeComment(commentInfo)

def user_callback(ch, method, properties, body):
    data = json.loads(body.decode('ASCII'))
    print("Update user_name ==> ", data)
    userInfo = schemas.UserModel(
        userId = data['userId'],
        userName = data['userName'],
        email = data['email'],
        bio = data['bio'],
        password = data['password'],
        occupation = data['occupation']
    )
    main.consumeUser(userInfo)

channel.basic_consume(queue='post_timeline', on_message_callback=post_callback, auto_ack=True)
channel.basic_consume(queue='react_timeline', on_message_callback=react_callback, auto_ack=True)
channel.basic_consume(queue='comment_timeline', on_message_callback=comment_callback, auto_ack=True)
channel.basic_consume(queue='user_timeline', on_message_callback=user_callback, auto_ack=True)

print("Timeline consumer")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
