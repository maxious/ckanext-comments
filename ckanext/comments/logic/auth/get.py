import logging
from pylons import config
from pylons.i18n import _

import ckanext.comments.model as comment_model
import ckanext.comments.logic as comment_logic
import ckan.logic.auth as ckanauth
import ckan.new_authz as new_authz
import ckan.lib.helpers as h
from ckan.lib.base import abort, c

log = logging.getLogger(__name__)


def thread_show(context, data_dict):
    model = context['model']
    user = context['user']
    return {'success': True}

def comment_show(context, data_dict):
    model = context['model']
    user = context['user']

    # If this user is a sysadmin, then yes.
    if new_authz.is_sysadmin(user):
        return {'success': True}

    # Otherwise this depends on state of the comment. If COMMENT_APPROVED
    # and state = 'active' then yes, otherwise, no.
    comment = comment_logic.get_comment(data_dict)
    if comment.approval_status == comment_model.COMMENT_APPROVED:
        return {'success': True}

    # If not approved, we only expect the author to see it.
    if c.userobj and comment.user == c.userobj:
        return {'success': True}

    return {'success': False, 'msg': _('You do not have permission to view this comment')}

def moderation_queue_show(context, data_dict):
    model = context['model']
    user = context['user']

    # Only if this user has the right to view the moderation queue,
    # typically only sysadmins.

    return {'success': False,
        'msg': _('You do not have permission to view the moderation queue')}
