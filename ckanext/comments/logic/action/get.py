import logging
from pylons import config
from pylons.i18n import _

import ckan.logic as logic
import ckan.new_authz as new_authz
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

def comment_show(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("comment_show", context, data_dict)

    return {}

def thread_show(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("thread_show", context, data_dict)

    return {}

def comment_list(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("comment_list", context, data_dict)

    return {}

