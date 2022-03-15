import pika
from fastapi import HTTPException
# from .database import SessionLocal
# from sqlalchemy.orm import Session


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    try:
        post_id = int(body.decode())
        print("postId ===> ", post_id, type(post_id))
        initiateReactsForPost(post_id)
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     except:
#         db.close()

# def initiateReactsForPost(post_id: int):
#     db: Session = get_db()
  
#     reactData = models.React(
#         postId = post_id,
#         smileReactCount = 0,
#         loveReactCount = 0,
#         likeReactCount = 0
#     )

#     try:
#         db.add(reactData)
#         db.commit()
#         db.refresh(reactData)

#         react_id = db.query(models.React).filter(models.React.postId == reactInfo.postId).first().reactId
#         return react_id
#     except:
#         raise HTTPException(status_code=500, detail="Internal server error")