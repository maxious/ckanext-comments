import datetime
import logging

from webhelpers.text import truncate

import ckan.plugins.toolkit as t
from ckan.lib.base import model, abort, response, h, BaseController, request
from ckan.controllers.api import ApiController
from ckan.lib.helpers import OrderedDict, date_str_to_datetime, markdown_extract, json
import ckanext.comments.model as comment_model

log = logging.getLogger(__name__)


class CommentApiController(ApiController):

    def thread(self, object_type, object_id):
        """
        Retrieves the thread for the specified object and returns
        it complete with comments.  If no thread exists then it 
        will be created as part of this request.
        """
        t = comment_model.CommentThread.get_or_create(object_type, object_id)


        return self._finish_ok({})

