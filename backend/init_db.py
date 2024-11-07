from sqlalchemy.sql import text
from db import create_database, get_session
from models import Comment, User, Publication, Tag, publication_tag_table
import logging
from uuid import UUID
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = create_database()
    # session = get_session()

    logger.info("Creating tables")

    User.__table__.create(session.get_bind(), checkfirst=True)
    Publication.__table__.create(session.get_bind(), checkfirst=True)
    Comment.__table__.create(session.get_bind(), checkfirst=True)
    Tag.__table__.create(session.get_bind(), checkfirst=True)
    publication_tag_table.create(session.get_bind(), checkfirst=True)


    users = [
        {"user_id": UUID('550e8400-e29b-41d4-a716-446655440000'), "username": 'user1', "email": 'user1@example.com'},
        {"user_id": UUID('550e8400-e29b-41d4-a716-446655440001'), "username": 'user2', "email": 'user2@example.com'}
    ]
    session.bulk_insert_mappings(User, users)

    publications = [
        {"publication_id": UUID('660e8400-e29b-41d4-a716-446655440000'), "title": 'Publication 1', "content": 'Content for publication 1', "user_id": UUID('550e8400-e29b-41d4-a716-446655440000'), "created_at": datetime.now()},
        {"publication_id": UUID('660e8400-e29b-41d4-a716-446655440001'), "title": 'Publication 2', "content": 'Content for publication 2', "user_id": UUID('550e8400-e29b-41d4-a716-446655440001'), "created_at": datetime.now()}
    ]
    session.bulk_insert_mappings(Publication, publications)

    comments = [
        {"comment_id": UUID('770e8400-e29b-41d4-a716-446655440000'), "content": 'Comment for publication 1', "user_id": UUID('550e8400-e29b-41d4-a716-446655440001'), "publication_id": UUID('660e8400-e29b-41d4-a716-446655440000'), "created_at": datetime.now()},
        {"comment_id": UUID('770e8400-e29b-41d4-a716-446655440001'), "content": 'Another comment for publication 2', "user_id": UUID('550e8400-e29b-41d4-a716-446655440000'), "publication_id": UUID('660e8400-e29b-41d4-a716-446655440001'), "created_at": datetime.now()}
    ]
    session.bulk_insert_mappings(Comment, comments)

    tags = [
        {"tag_id": UUID('880e8400-e29b-41d4-a716-446655440000'), "name": 'F3'},
        {"tag_id": UUID('880e8400-e29b-41d4-a716-446655440001'), "name": 'Profesores'},
        {"tag_id": UUID('880e8400-e29b-41d4-a716-446655440002'), "name": 'Cloud'},
        {"tag_id": UUID('880e8400-e29b-41d4-a716-446655440003'), "name": 'AWS'}
    ]
    session.bulk_insert_mappings(Tag, tags)


    session.commit()
    session.close()

    logger.info("Tables created successfully")

    return {
        'statusCode': 200,
        'body': 'Tables created successfully'
    }
