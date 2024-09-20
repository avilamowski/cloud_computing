from db import get_session
from models import Comment, User
import json

def lambda_handler(event, context):
    session = get_session()

    try:
        publication_id = event.get('queryStringParameters', {}).get('publication_id')
        page = event.get('queryStringParameters', {}).get('page', 1)

        if not publication_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'publication_id is required'})
            }
        
        if not page.isdigit() or int(page) < 1:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'invalid page'})
            }
        
        comments = session.query(Comment).filter_by(publication_id=publication_id).limit(10).offset((int(page) - 1) * 10).all()

        result = []
        for comment in comments:
            result.append({
                'comment_id': comment.comment_id,
                'content': comment.content,
                'user_id': comment.user_id,
                'username': comment.user.username, 
                'created_at': comment.created_at.isoformat()
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
