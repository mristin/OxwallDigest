__author__ = 'marko'

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
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

# CREATE TABLE `ow_forum_post` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `topicId` int(11) NOT NULL,
#   `userId` int(11) NOT NULL,
#   `text` text NOT NULL,
#   `createStamp` int(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `topicId` (`topicId`),
#   FULLTEXT KEY `post_text` (`text`)
# ) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
