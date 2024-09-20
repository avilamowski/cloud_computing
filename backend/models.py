from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(String, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    publication_id = Column(String, ForeignKey('publications.publication_id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)

    # user = relationship("User", back_populates="comments")
    # publication = relationship("Publication", back_populates="comments")

class Publication(Base):
    __tablename__ = 'publications'
    publication_id = Column(String, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)

    # comments = relationship("Comment", back_populates="publication")

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
