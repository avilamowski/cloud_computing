from db import get_session
from models import Publication
import json
from sqlalchemy.orm import joinedload


def lambda_handler(event, context):
    session = get_session()

    try:
        if event:
            search_term = event.get('queryStringParameters', {}).get('search_term')
            page = event.get('queryStringParameters', {}).get('page', 1)
        else:
            search_term = None
            page = 1

        if not str(page).isdigit() or int(page) < 1:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'invalid page'})
            }

        publication_query = session.query(Publication)
        if search_term:
            publication_query = \
                publication_query.filter(Publication.title.ilike(f'%{search_term}%') | Publication.content.ilike(f'%{search_term}%'))

        # publications = publication_query.limit(10).offset((int(page) - 1) * 10).all()
        # get publications and user data
        publications = publication_query.limit(10).offset((int(page) - 1) * 10).options(joinedload(Publication.user)).all()

        result = [ pub.to_dict() for pub in publications ]
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
