from db import get_session
from models import Publication, User, Tag
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
        tags = data.get('tags', [])  # Obtener los tags del cuerpo de la solicitud
        claims = event['requestContext']['authorizer']['claims']
        email = claims['email']

        if not title or not content or not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'title, content are required'})
            }

        if not isinstance(tags, list) or len(tags) > 5:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Tags must be a list with a maximum of 5 items'})
            }

        user = session.query(User).filter_by(email=email).first()
        if not user:
            logger.error("User not found")
            return {
                'statusCode': 400,
                'body': 'User not found'
            }

        logger.info(f'User: {user.user_id}')

        # Crear nueva publicación
        new_publication = Publication(
            publication_id=str(uuid.uuid4()), 
            title=title,
            content=content,
            user_id=user.user_id,
            created_at=datetime.datetime.now()
        )

        # Procesar tags
        tag_objects = []
        for tag_name in tags:
            tag_name = tag_name.strip().lower()  # Normalizar el nombre del tag
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(tag_id=str(uuid.uuid4()), name=tag_name)
                session.add(tag)
            tag_objects.append(tag)

        new_publication.tags.extend(tag_objects)

        logger.info(f'Publication: {new_publication.publication_id}')
        session.add(new_publication)
        session.commit()

        publication_id = str(new_publication.publication_id)

        session.close()

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Publication created successfully',
                'publication_id': publication_id,
            })
        }

    except Exception as e:
        session.close()
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
