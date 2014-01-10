import logging
from pylons import config
from pylons.i18n import _

import ckanext.comments.model as comment_model
import ckan.logic as logic
import ckan.new_authz as new_authz
import ckan.lib.helpers as h
from ckan.lib.base import abort, c

log = logging.getLogger(__name__)

def comment_create(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("comment_create", context, data_dict)

    # Validate that we have the required fields.
    if not all([data_dict.get('thread_id'),
                data_dict.get('comment')]):
        raise logic.ValidationError("Both thread_id and comment are required")

    # Clean the comment
    cleaned_comment = data_dict.get('comment')
    formatted_comment = cleaned_comment

    # Create the object
    cmt = comment_model.Comment(thread_id=data_dict.get('thread_id'),
                              comment=cleaned_comment,
                              comment_formatted=formatted_comment)
    cmt.parent_id = data_dict.get('parent_id')
    cmt.user_id = c.userobj.id
    if new_authz.is_sysadmin(user):
        cmt.approval_status = comment_model.COMMENT_APPROVED
        cmt.moderated_by = c.userobj.id
        cmt.spam_checked = 1
    else:
        cmt.approval_status = comment_model.COMMENT_PENDING

    model.Session.add(cmt)
    model.Session.commit()

    # Queue for spam checking.


    return cmt.as_dict()
