"""
The FeedbackController is responsible for processing requests related to the
unpublished feedback that allows users and admins to record feedback in a
specific format against unpublished datasets.
"""
import logging
import json
from ckan import model
from paste.deploy.converters import asbool
from ckan.lib.base import h, BaseController, abort
from ckanext.dgu.plugins_toolkit import (render, c, request, _,
                                         ObjectNotFound, NotAuthorized,
                                         get_action, check_access)
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.logic import tuplize_dict, clean_dict, parse_params, flatten_to_string_key, ValidationError

log = logging.getLogger(__name__)


class CommentController(BaseController):

    def add(self, dataset_name):
        c.action = 'add'
        return self._add_or_reply(dataset_name)

    def reply(self, dataset_name, parent_id):
        c.action = 'reply'

        try:
            data = {'id': parent_id}
            c.parent_dict = get_action("comment_show")({'model': model, 'user': c.user},
                data)
            c.parent = data['comment']
        except:
            abort(404)

        return self._add_or_reply(dataset_name)


    def _add_or_reply(self, dataset_name):
        """
        Allows the user to add a comment to an existing dataset
        """
        context = {'model':model,'user': c.user}

        # Auth check to make sure the user can see this package
        ctx = context
        ctx['id'] = dataset_name
        check_access('package_show', ctx)

        try:
            c.pkg_dict = get_action('package_show')(context, {'id': dataset_name})
            c.pkg = context['package']
        except:
            abort(403)

        errors = {}

        if request.method == 'POST':
            data_dict = clean_dict(unflatten(
                tuplize_dict(parse_params(request.POST))))
            data_dict['parent_id'] = c.parent.id if c.parent else None
            data_dict['url'] = '/dataset/%s' % c.pkg.name

            success = False
            try:
                res = get_action('comment_create')(context, data_dict)
                success = True
            except ValidationError, ve:
                errors = ve.error_dict
            except Exception, e:
                abort(403)

            if success:
                h.redirect_to(str('/dataset/%s#comment_%s' % (c.pkg.name, res['id'])))

        vars = {'errors': errors}

        # TODO: Check if user is in BlockedUsers, if so discard any input
        c.form = render('comments/create_form.html', extra_vars=vars)

        return render('comments/create.html')

