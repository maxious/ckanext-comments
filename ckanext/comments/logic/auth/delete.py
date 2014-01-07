import logging
from pylons import config
from pylons.i18n import _

import ckan.new_authz as new_authz
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

def comment_delete(context, data_dict):
    model = context['model']
    user = context['user']

    # If sysadmin.
    if new_authz.is_sysadmin(user):
        return {'success': True}

    return {'success': False,
        'msg': _('You do not have permission to delete this comment')}
