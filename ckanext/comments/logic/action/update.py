import logging
from pylons import config
from pylons.i18n import _

import ckan.logic as logic
import ckan.new_authz as new_authz
import ckan.lib.helpers as h
import datetime
from ckan.lib.base import abort, c

log = logging.getLogger(__name__)

def comment_update(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("comment_update", context, data_dict)

    return {}
def comment_update_approve(context, data_dict):
    import ckanext.comments.model as comment_model

    model = context['model']
    user = context['user']

    cid = logic.get_or_bust(data_dict, 'id')
    comment = comment_model.Comment.get(cid)
    if not comment:
        abort(404)

    # If sysadmin, then remove instantly
    if c.userobj.sysadmin:
        comment.approval_status = comment_model.COMMENT_APPROVED
        comment.moderated_by = c.userobj.id
        comment.moderation_date = datetime.datetime.now()
        model.Session.add(comment)
        model.Session.commit()

    return {}

def comment_update_moderation(context, data_dict):
    import ckanext.comments.model as comment_model

    model = context['model']
    user = context['user']

    cid = logic.get_or_bust(data_dict, 'id')
    comment = comment_model.Comment.get(cid)
    if not comment:
        abort(404)

    # If sysadmin, then remove instantly
    if c.userobj.sysadmin:
        if len(comment.children) > 0:
            txt = config.get('ckan.comments.deleted.text', 'This message was deleted')
            comment.comment = txt
        else:
            comment.state = 'deleted'
        comment.approval_status = comment_model.COMMENT_PENDING
        comment.moderated_by = c.userobj.id
        comment.moderation_date = datetime.datetime.now()
        model.Session.add(comment)
        model.Session.commit()
    elif not comment.moderated_by:
        comment.spam_votes = comment.spam_votes + 1
        comment.approval_status = comment_model.COMMENT_PENDING
        model.Session.add(comment)
        model.Session.commit()

    return {}

def moderation_queue_update(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("moderation_queue_update", context, data_dict)

    return {}