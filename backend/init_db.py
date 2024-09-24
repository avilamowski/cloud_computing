from sqlalchemy.sql import text
from db import create_database
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = create_database()

    logger.info("Creating tables")

    queries = text("""
    CREATE TABLE users(
        user_id UUID PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );

    CREATE TABLE publications(
        publication_id UUID PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id UUID NOT NULL REFERENCES users(user_id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE comments(
        comment_id UUID PRIMARY KEY,
        content TEXT NOT NULL,
        user_id UUID NOT NULL REFERENCES users(user_id),
        publication_id UUID NOT NULL REFERENCES publications(publication_id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE tags(
        tag_id SERIAL PRIMARY KEY,
        tag_name VARCHAR(100) NOT NULL
    );

    CREATE TABLE publications_tags(
        publication_id UUID NOT NULL REFERENCES publications(publication_id),
        tag_id SERIAL NOT NULL REFERENCES tags(tag_id),
        PRIMARY KEY(publication_id, tag_id)
    );

    -- Insert users
    INSERT INTO users (user_id, username, email)
    VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'user1', 'user1@example.com'),
    ('550e8400-e29b-41d4-a716-446655440001', 'user2', 'user2@example.com');

    -- Insert publications
    INSERT INTO publications (publication_id, title, content, user_id)
    VALUES
    ('660e8400-e29b-41d4-a716-446655440000', 'Publication 1', 'Content for publication 1', '550e8400-e29b-41d4-a716-446655440000'),
    ('660e8400-e29b-41d4-a716-446655440001', 'Publication 2', 'Content for publication 2', '550e8400-e29b-41d4-a716-446655440001');

    -- Insert comments
    INSERT INTO comments (comment_id, content, user_id, publication_id)
    VALUES
    ('770e8400-e29b-41d4-a716-446655440000', 'Comment for publication 1', '550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440000'),
    ('770e8400-e29b-41d4-a716-446655440001', 'Another comment for publication 2', '550e8400-e29b-41d4-a716-446655440000', '660e8400-e29b-41d4-a716-446655440001');

    -- Insert tags
    INSERT INTO tags (tag_name)
    VALUES
    ('Technology'),
    ('Science');

    -- Insert publications_tags
    INSERT INTO publications_tags (publication_id, tag_id)
    VALUES
    ('660e8400-e29b-41d4-a716-446655440000', 1),
    ('660e8400-e29b-41d4-a716-446655440001', 2);
    """)

    session.execute(queries)
    session.close()

    logger.info("Tables created successfully")

    return {
        'statusCode': 200,
        'body': 'Tables created successfully'
    }
