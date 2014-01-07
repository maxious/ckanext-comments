import logging
from pylons import config
from pylons.i18n import _

import ckan.logic as logic
import ckan.new_authz as new_authz
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

def comment_create(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("comment_create", context, data_dict)

    return {}

def thread_create(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("thread_create", context, data_dict)

    return {}