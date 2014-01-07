import uuid
import datetime

from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import types, orm
from sqlalchemy.sql import select
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

from ckan.plugins import toolkit

import ckan.model as model
from ckan.lib.base import *

log = __import__('logging').getLogger(__name__)

Base = declarative_base()
metadata = MetaData()

COMMENT_APPROVED = "approved"
COMMENT_PENDING = "pending"
COMMENT_DELETED = "deleted"

def make_uuid():
    return unicode(uuid.uuid4())

def acceptable_comment_on(objtype):
    return objtype in ['package']

class CommentThread(Base):
    """
    Represents a thread, or in this particular case a collection of
    comments against a CKAN object.  This is the container for the
    """
    __tablename__ = 'comment_thread'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)

    comment_on = Column(types.UnicodeText)
    comment_on_id = Column(types.UnicodeText)

    creation_date = Column(types.DateTime, default=datetime.datetime.now)

    locked = Column(types.Boolean, default=False)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get_or_create(cls, obj, id):
        """
        Retrieves the thread for the specified object if any exists. If
        no thread currently exists, one is created for that object.
        """
        thread = model.Session.query(cls).\
            filter(cls.comment_on==obj).\
            filter(cls.comment_on_id==id).first()
        if not thread:
            if not acceptable_comment_on(obj):
                return None
            thread = CommentThread(comment_on=obj, comment_on_id=id)
            model.Session.add(thread)
            model.Session.commit()
        return thread


class Comment(Base):
    """
    A comment is a text block provided by a user against an object, or in this
    particular case a CommentThread (one per object). Comments *might* be threaded
    based on configuration, and may or may not be moderated.
    """
    __tablename__ = 'comment'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    parent_id = Column(types.UnicodeText, ForeignKey('comment.id'))
    children = relationship("Comment", lazy="joined", join_depth=10,
                backref=backref('parent', remote_side=[id]))

    thread_id = Column(types.UnicodeText, ForeignKey('comment_thread.id'), nullable=True)
    user_id = Column(types.UnicodeText, ForeignKey(model.User.id), nullable=False)
    comment = Column(types.UnicodeText)

    creation_date = Column(types.DateTime, default=datetime.datetime.now)
    approval_status = Column(types.UnicodeText)

    moderation_date = Column(types.DateTime)
    moderated_by = Column(types.UnicodeText, ForeignKey(model.User.id), nullable=False)

    spam_votes = Column(types.Integer, default=0)
    spam_score = Column(types.Integer, default=0)
    spam_checked = Column(types.Integer, default=0)

    state = Column(types.UnicodeText)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

        # Auto-set some values based on configuration
        from pylons import config
        if toolkit.asbool(config.get('ckan.comments.moderation', 'true')):
            self.approval_status = COMMENT_PENDING
        else:
            # If user wants first comment moderated and the user who wrote this hasn't
            # got another comment, put it into moderation, otherwise approve
            if toolkit.asbool(config.get('ckan.comments.moderation.first_only', 'true')) and \
                  Comment.count_for_user(self.user, COMMENT_APPROVED) == 0:
                self.approval_status = COMMENT_PENDING
            else:
                self.approval_status = COMMENT_APPROVED

    @classmethod
    def count_for_user(cls, user, status):
        return model.Session.query(Comment)\
            .filter(Comment.approval_status==status)\
            .filter(Comment.user==user).count()

def init_tables():
    Base.metadata.create_all(model.meta.engine)

