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

    user = relationship("User", back_populates="comments")
    # publication = relationship("Publication", back_populates="comments")

    def to_dict(self):
        return {
            'comment_id': str(self.comment_id),
            'content': self.content,
            'user_id': str(self.user_id),
            'publication_id': str(self.publication_id),
            'created_at': self.created_at.isoformat()
        }

class Publication(Base):
    __tablename__ = 'publications'
    publication_id = Column(String, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)

    # comments = relationship("Comment", back_populates="publication")
    def to_dict(self):
        return {
            'publication_id': str(self.publication_id),
            'title': self.title,
            'content': self.content,
            'user_id': str(self.user_id),
            'created_at': self.created_at.isoformat()
        }

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    comments = relationship("Comment", back_populates="user")

    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'username': self.username,
            'email': self.email
        }
