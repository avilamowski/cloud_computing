from db import get_session
from models import Publication, User
import json
import uuid
import datetime

def lambda_handler(event, context):
    session = get_session()

    try:
        data = json.loads(event['body'])

        title = data.get('title')
        content = data.get('content')
        username = data.get('username') # TODO: Only get user id in future implementation
        email = data.get('email') # TODO: Only get user id in future implementation

        if not title or not content or not username or not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'title, content and username are required'})
            }

        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(
                user_id=str(uuid.uuid4()),
                username=username,
                email=email
            )
            session.add(user)

        new_publication = Publication(
            publication_id=str(uuid.uuid4()), 
            title=title,
            content=content,
            user_id=user.user_id,
            created_at=datetime.datetime.now()
        )

        session.add(new_publication)
        session.commit()

        session.close()

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Publication created successfully',
                'publication_id': new_publication.publication_id
            })
        }

    except Exception as e:
        session.close()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
