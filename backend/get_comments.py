from db import get_session
from models import Comment, User
from sqlalchemy.orm import joinedload
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = get_session()
    logger.info("Event: %s", event)

    try:
        # publication_id = event.get('pathParameters').get('publication_id')
        publication_id = event.get('queryStringParameters', {}).get('publication_id')
        page = event.get('queryStringParameters', {}).get('page', 1)

        if not publication_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'publication_id is required'})
            }
        
        if not str(page).isdigit() or int(page) < 1:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'invalid page'})
            }
        
        comments = session.query(Comment).filter_by(publication_id=publication_id).limit(10).offset((int(page) - 1) * 10).options(joinedload(Comment.user)).all()

        result = [ comment.to_dict() for comment in comments ]
        session.close()

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        session.close()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
