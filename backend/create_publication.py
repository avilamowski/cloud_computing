from db import get_session
from models import Publication, User
import json
import uuid
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = get_session()
    logger.info(event)

    try:
        data = json.loads(event.get('body'))
        title = data.get('title')
        content = data.get('content')
        username = data.get('username') # TODO: Only get user id in future implementation
        email = data.get('email') # TODO: Only get user id in future implementation

        if not title or not content or not username or not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'title, content and username are required'})
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

        logger.info(f'User: {user.user_id}')

        new_publication = Publication(
            publication_id=str(uuid.uuid4()), 
            title=title,
            content=content,
            user_id=user.user_id,
            created_at=datetime.datetime.now()
        )

        logger.info(f'Publication: {new_publication.publication_id}')
        session.add(new_publication)
        session.commit()

        publication_id = str(new_publication.publication_id)

        session.close()

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Publication created successfully',
                'publication_id': publication_id
            })
        }

    except Exception as e:
        session.close()
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
