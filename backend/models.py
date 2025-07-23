from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Recipient(Base):
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship('Group', back_populates='recipients')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    recipients = relationship('Recipient', back_populates='group')

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)  # e.g. "Hi {name}, ..."
    media_id = Column(Integer, ForeignKey('media.id'), nullable=True)
    media = relationship('Media', back_populates='templates')

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'))
    template = relationship('Template')
    recipient_id = Column(Integer, ForeignKey('recipients.id'), nullable=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    send_time = Column(DateTime, nullable=False)
    recurring = Column(Boolean, default=False)
    interval = Column(String, nullable=True)  # e.g. 'daily', 'weekly', cron string
    active = Column(Boolean, default=True)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    recipient_id = Column(Integer, ForeignKey('recipients.id'))
    status = Column(String, nullable=False)  # sent, failed, etc.
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # image, audio, video
    templates = relationship('Template', back_populates='media') 