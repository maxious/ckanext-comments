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

    return {'success': True, 'msg': _('')}

def thread_update(context, data_dict):
    model = context['model']
    user = context['user']

    return {'success': True, 'msg': _('')}