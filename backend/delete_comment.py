from db import get_session
from models import Comment, User
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = get_session()
    logger.info("Event: %s", event)
    try:
        data = json.loads(event['body'])

   
        claims = event['requestContext']['authorizer']['claims']
        email = claims['email']
        comment_id = data.get('comment_id')

        if not email or not comment_id:
            session.close()
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'comment_id is required'})
            }
            
        if not "admin-group" in claims['cognito:groups']:
            logger.error("Forbidden")
            session.close()
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Forbidden'})
            }


        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            session.close()
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Comment not found'})
            }
        

        session.delete(comment)
        session.commit()

        session.close()

        logger.info(f'Comment deleted: {comment_id}')

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Comment deleted successfully'
            })
        }

    except Exception as e:
        session.close()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }