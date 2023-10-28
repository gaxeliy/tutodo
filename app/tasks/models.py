import datetime
import uuid

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, UUID

from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    scheduled_at = Column(DateTime)
    my_day_date = Column(Date)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)


class TaskTag(Base):
    __tablename__ = 'task_tags'
    id = Column(Integer, autoincrement=True, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'))
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'))


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)


class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    task_id = ForeignKey('tasks.id', ondelete='CASCADE')
    remind_at = Column(DateTime)
