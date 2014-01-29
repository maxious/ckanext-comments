import logging
from pylons import config
from pylons.i18n import _

import ckan.new_authz as new_authz
import ckan.lib.helpers as h
from ckan.lib.base import abort, c

log = logging.getLogger(__name__)

def comment_create(context, data_dict):
    from ckanext.comments.model import CommentBlockedUser
    user = context['user']
    model = context['model']

    userobj = model.User.get(user)

    if not userobj:
        log.debug("User is not logged in")
        return {'success': False, 'msg': _('You must be logged in to add a comment')}

    if model.Session.query(CommentBlockedUser)\
            .filter(CommentBlockedUser.user==userobj).count() > 0:
        return {'success': False, 'msg': _('User is blocked')}

    return {'success': True }
