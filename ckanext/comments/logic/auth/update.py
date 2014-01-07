import logging
from pylons import config
from pylons.i18n import _

import ckan.logic as logic
import ckan.new_authz as new_authz
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

def comment_update(context, data_dict):
    model = context['model']
    user = context['user']

    # If sysadmin, then yes.
    if new_authz.is_sysadmin(user):
        return {'success': True}

    # If owner, then yes in theory but we don't really want people changing
    # the contents of earlier posts. We should restrict update to not changing
    # the content itself.

    return {'success': False, 'msg': _('You do not have permission to update this comment')}

def moderation_queue_update(context, data_dict):
    model = context['model']
    user = context['user']

    # Sysadmins only

    return {'success': False,
        'msg': _('You do not have permission to update the moderation queue')}