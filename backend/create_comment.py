from db import get_session
from models import Comment, User
import json
import uuid
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = get_session()
    logger.info("Event: %s", event)

    try:
        data = json.loads(event['body'])

        content = data.get('content')
        username = data.get('username')
        email = data.get('email')
        publication_id = data.get('publication_id')


        if not content or not username or not email or not publication_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'content, user_id, and publication_id are required'})
            }
            
        user = session.query(User).filter_by(username=username).filter_by(email=email).first()
        if not user:
            try:
                user = User(
                    user_id=str(uuid.uuid4()),
                    username=username,
                    email=email
                )
                session.add(user)
                session.commit()
            except Exception as e:
                logger.error("Error creating user: there was already a user with the same username or email")
                return {
                    'statusCode': 500,
                    'body': 'There was already a user with the same username or email'
                }
                

        new_comment = Comment(
            comment_id=str(uuid.uuid4()),
            content=content,
            user_id=user.user_id,
            publication_id=publication_id,
            created_at=datetime.datetime.now()
        )
        

        session.add(new_comment)
        session.commit()

        new_comment_id = str(new_comment.comment_id)
        session.close()

        logger.info(f'Comment: {new_comment_id}')

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Comment created successfully',
                'comment_id': new_comment_id
            })
        }

    except Exception as e:
        session.close()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
