import logging
from pylons import config
from pylons.i18n import _

import ckan.logic as logic
import ckanext.comments.model as comment_model
import ckan.new_authz as new_authz
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import abort

log = logging.getLogger(__name__)


def thread_show(context, data_dict):
    model = context['model']
    user = context['user']

    url = logic.get_or_bust(data_dict, 'url')
    thread = comment_model.CommentThread.from_url(url)
    if not thread:
        return abort(404)

    data_dict['thread'] = thread
    logic.check_access("thread_show", context, data_dict)

    # Dictize the thread and all the comments within it.
    thread_dict = thread.as_dict()

    # Add the 'threaded' comments in order to the following list.
    # TODO: Allow call to specify from which comment onwards they want
    # to retrieve, and how many.
    thread_dict['comments'] = []

    return thread_dict


def comment_show(context, data_dict):
    model = context['model']
    user = context['user']

    id = logic.get_or_bust(data_dict, 'id')
    comment = comment_model.Comment.get(id)
    if not comment:
        abort(404)

    data_dict['comment'] = comment
    logic.check_access("comment_show", context, data_dict)

    return {}

def moderation_queue_show(context, data_dict):
    model = context['model']
    user = context['user']

    logic.check_access("moderation_queue_show", context, data_dict)

    return {}