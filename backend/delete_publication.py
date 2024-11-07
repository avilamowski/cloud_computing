from db import get_session
from models import Publication, User
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
        publication_id = data.get('publication_id')

        if not email or not publication_id:
            session.close()
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'publication_id is required'})
            }
            
        if not "admin-group" in claims['cognito:groups']:
            logger.error("Forbidden")
            session.close()
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Forbidden'})
            }
                

        publication = session.query(Publication).filter_by(publication_id=publication_id).first()
        if not publication:
            session.close()
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Publication not found'})
            }
        

        session.delete(publication)
        session.commit()

        session.close()

        logger.info(f'Publication deleted: {publication_id}')

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Publication deleted successfully'
            })
        }

    except Exception as e:
        session.close()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }