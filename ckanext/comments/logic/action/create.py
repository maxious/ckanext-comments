import logging
from pylons import config
from pylons.i18n import _

import ckanext.comments.util as util
import ckanext.comments.model as comment_model
import ckan.logic as logic
import ckan.new_authz as new_authz
import ckan.lib.helpers as h
from ckan.lib.base import abort, c
from ckan.plugins import toolkit

log = logging.getLogger(__name__)

def comment_create(context, data_dict):
    model = context['model']
    user = context['user']

    userobj = model.User.get(user)

    logic.check_access("comment_create", context, data_dict)

    # Validate that we have the required fields.
    if not all([data_dict.get('comment')]):
        raise logic.ValidationError("Comment is required")

    thread_id = data_dict.get('thread_id')
    if not thread_id:
        url = data_dict.get('url')
        if url:
            thread = comment_model.CommentThread.from_url(url)
            thread_id = thread.id if thread else None

    if not thread_id:
        raise logic.ValidationError("Thread identifier or URL is required")

    # TODO: Clean the comment
    cleaned_comment = util.clean_input(data_dict.get('comment'))
    formatted_comment = util.format_comment(cleaned_comment)

    # Create the object
    cmt = comment_model.Comment(thread_id=thread_id,
                              comment=cleaned_comment,
                              comment_formatted=formatted_comment)
    cmt.user_id = userobj.id

    prt = data_dict.get('parent_id')
    if prt:
        parent = comment_model.Comment.get(prt)
        if parent:
            cmt.parent_id = parent.id

    # Sysadmins get auto-approve, auto-moderate.
    if new_authz.is_sysadmin(user):
        cmt.approval_status = comment_model.COMMENT_APPROVED
        cmt.moderated_by = userobj.id
        cmt.spam_checked = 1
    else:
        # If we want to force moderation of first comment from each user
        # otherwise it will be every comment.
        cmt.approval_status = comment_model.COMMENT_PENDING

        if toolkit.asbool(config.get('ckan.comments.moderation.first_only')):
            if comment_model.Comment.count_for_user(user) != 0:
                cmt.approval_status = comment_model.COMMENT_APPROVED

    # We only allow parent_id to be set if we want threaded comments.  If we do not
    # then we will just post this as a normal comment.
    if toolkit.asbool(config.get('ckan.comments.threaded', False)):
        cmt.parent_id = data_dict.get('parent_id')

    model.Session.add(cmt)
    model.Session.commit()

    # Queue for spam checking.


    return cmt.as_dict()
