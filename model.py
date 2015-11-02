__author__ = 'marko'

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define models
Base = sqlalchemy.ext.declarative.declarative_base()


class User(Base):
    __tablename__ = "ow_base_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    email = Column(String(128), nullable=False)


class Forum_section(Base):
    __tablename__ = 'ow_forum_section'
    id = Column(Integer, primary_key=True)
    is_hidden = Column('isHidden', Boolean, nullable=True)


class Forum_group(Base):
    __tablename__ = 'ow_forum_group'
    id = Column(Integer, primary_key=True)
    is_private = Column('isPrivate', Boolean, nullable=True)
    name = Column('name', Text, nullable=False)
    section_id = Column('sectionId', ForeignKey('ow_forum_section.id'), nullable=False)

    section = relationship(Forum_section)


class Forum_topic(Base):
    __tablename__ = "ow_forum_topic"
    id = Column(Integer, primary_key=True)
    title = Column('title', Text, nullable=False)
    user_id = Column('userId', Integer, ForeignKey('ow_base_user.id'), nullable=False)
    group_id = Column('groupId', Integer, ForeignKey('ow_forum_group.id'), nullable=False)

    user = relationship(User)
    group = relationship(Forum_group)


class Forum_post(Base):
    __tablename__ = "ow_forum_post"
    id = Column('id', Integer, primary_key=True)
    topic_id = Column('topicId', Integer, ForeignKey('ow_forum_topic.id'), nullable=False)
    create_stamp = Column('createStamp', Integer, nullable=False)
    text = Column('text', Text, nullable=False)
    user_id = Column('userId', Integer, ForeignKey('ow_base_user.id'), nullable=False)

    topic = relationship(Forum_topic)
    user = relationship(User)


class Blog_post(Base):
    __tablename__ = "ow_blogs_post"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('authorId', Integer, ForeignKey('ow_base_user.id'), nullable=False)
    title = Column('title', String(512), nullable=False)
    post = Column('post', Text, nullable=False)
    timestamp = Column('timestamp', Integer, nullable=False)
    is_draft = Column('isDraft', Boolean, nullable=False)
    privacy = Column('privacy', String(50), nullable=False, default="everybody")

    user = relationship(User)


class Event(Base):
    __tablename__ = "ow_event_item"
    id = Column('id', Integer, primary_key=True)
    title = Column('title', Text, nullable=False)
    create_timestamp = Column('createTimeStamp', Integer, nullable=False)
    user_id = Column('userId', Integer, ForeignKey('ow_base_user.id'), nullable=False)
    who_can_view = Column("whoCanView", TINYINT(4), nullable=False)

    user = relationship(User)

class Comment_entity(Base):
    __tablename__ = "ow_base_comment_entity"
    id = Column("id", Integer, primary_key=True)
    entity_type = Column('entityType', String(255), nullable=True)
    entity_id =  Column("entityId", Integer)
    active = Column("active", TINYINT(4))

class Comment(Base):
    __tablename__ = "ow_base_comment"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('userId', Integer, ForeignKey('ow_base_user.id'), nullable=False)
    comment_entity_id = Column('commentEntityId', Integer, ForeignKey('ow_base_comment_entity.id'), nullable=False)
    create_stamp = Column('createStamp', Integer, nullable=False)

    user = relationship(User)
    comment_entity = relationship(Comment_entity)