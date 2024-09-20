from db import get_session
from models import Publication
import json

def lambda_handler(event, context):
    session = get_session()

    try:
        search_term = event.get('queryStringParameters', {}).get('search_term')
        page = event.get('queryStringParameters', {}).get('page', 1)

        # if not page.isdigit() or int(page) < 1:
        #     return {
        #         'statusCode': 400,
        #         'body': json.dumps({'error': 'invalid page'})
        #     }

        publication_query = session.query(Publication)
        if search_term:
            publication_query = \
                publication_query.filter(Publication.title.ilike(f'%{search_term}%') | Publication.content.ilike(f'%{search_term}%'))

        publications = publication_query.limit(10).offset((int(page) - 1) * 10).all()

        result = []
        for pub in publications:
            result.append({
                'publication_id': str(pub.publication_id),
                'title': pub.title,
                'content': pub.content,
                'user_id': str(pub.user_id),
                'created_at': pub.created_at.isoformat()
            })

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
