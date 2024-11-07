import json
import re
import boto3
import logging
import os
from db import get_session
from models import Comment, Publication

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

BUCKET_NAME = os.environ.get('SPAM_BUCKET_NAME')
SPAM_TOPIC_ARN = os.environ.get('SPAM_TOPIC_ARN')
EN_FILE_KEY = 'en.txt'
ES_FILE_KEY = 'es.txt'

def lambda_handler(event, context):
    logger.info('Event: %s', event)
    session = get_session()
    try:
        banned_words = load_banned_words_from_s3()
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, banned_words)) + r')\b', re.IGNORECASE)

        for record in event['Records']:
            message = json.loads(record['body'])
            item_id = message['id']
            item_type = message['type']

            name, content = get_content_by_id(session, item_id, item_type)
            if not content:
                logger.error(f'{item_type.capitalize()} with ID {item_id} not found')
                continue

            if pattern.search(content):
                logger.info(f'Possible spam detected in {item_type} with ID {item_id}')
                notify_moderators(item_id, item_type, name)

        session.close()
    except Exception as e:
        session.close()
        logger.error(e)
        raise e

def load_banned_words_from_s3():
    logger.info(f"Cargando palabras prohibidas del bucket {BUCKET_NAME} archivos {EN_FILE_KEY} y {ES_FILE_KEY}")
    try:
        en_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=EN_FILE_KEY)
        es_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=ES_FILE_KEY)
        logger.info('Palabras prohibidas leidas de S3')

        en_content = en_response['Body'].read().decode('utf-8')
        es_content = es_response['Body'].read().decode('utf-8')
        logger.info('Contenido leido de los archivos')

        banned_words = [line.strip() for line in en_content.split('\n') + es_content.split('\n') if line.strip()]
        logger.info(f'Cargadas {len(banned_words)} palabras prohibidas.')
        return banned_words
    except Exception as e:
        logger.error(f'Error al cargar las palabras prohibidas: {e}')
        return []

def get_content_by_id(session, item_id, item_type):
    logger.info(f'Obteniendo contenido por ID... ({item_type} {item_id})')
    if item_type == 'comment':
        comment = session.query(Comment).filter_by(comment_id=item_id).first()
        comment_publication_name = comment.publication.title if comment else None
        comment_content = comment.content if comment else None
        return comment_publication_name, comment_content
    elif item_type == 'publication':
        publication = session.query(Publication).filter_by(publication_id=item_id).first()
        publication_name = publication.title if publication else None
        publication_content = publication.content if publication else None
        return publication_name, publication_content
    return None

def notify_moderators(item_id, item_type, item_name):
    try:
        sns_client.publish(
            TopicArn=SPAM_TOPIC_ARN,
            Subject=f'Spam Alert in {item_type.capitalize()}',
            Message=f'Potential spam detected {item_type} with ID {item_id}, name: {item_name}'
        )
        logger.info(f'Notification sent for {item_type} with ID {item_id}')
    except Exception as e:
        logger.error(f'Error sending notification for {item_type} with ID {item_id}: {e}')

