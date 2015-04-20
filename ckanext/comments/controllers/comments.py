"""
The FeedbackController is responsible for processing requests related to the
unpublished feedback that allows users and admins to record feedback in a
specific format against unpublished datasets.
"""
import logging
import json
from ckan import model
from paste.deploy.converters import asbool
from ckan.lib import mailer
from ckan.lib.base import h, BaseController, abort
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.logic import tuplize_dict, clean_dict, parse_params, flatten_to_string_key, ValidationError
from pylons import config

import ckan.plugins.toolkit as tk
import ckanext.comments.model as comment_model

log = logging.getLogger(__name__)

import ckan.plugins.toolkit as t

_ = t._
c = t.c
request = t.request
render = t.render
render_text = t.render_text
asbool = t.asbool
asint = t.asint
aslist = t.aslist
literal = t.literal

get_action = t.get_action
check_access = t.check_access
ObjectNotFound = t.ObjectNotFound
NotAuthorized = t.NotAuthorized
ValidationError = t.ValidationError

CkanCommand = t.CkanCommand


class CommentController(BaseController):
    def moderation(self):
        context = {'model': model, 'user': c.user}
        check_access('moderation_queue_show', context)

        try:
            res = get_action('moderation_queue_show')(context, {})
        except Exception, e:
            abort(403)

        c.comments = res.get('comments')
        for comment in c.comments:
            comment['thread'] = comment_model.CommentThread.get(comment['thread_id'])
            comment['dataset'] = model.Package.get(comment['thread'].url.replace('/dataset/',''))

        return render('comments/moderation.html')


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

    def flag(self, dataset_name, id):
        context = {'model': model, 'user': c.user}

        try:
            c.pkg_dict = get_action('package_show')(context, {'id': dataset_name})
            c.pkg = context['package']
        except Exception, e:
            abort(403)

        try:
            get_action('comment_update_moderation')(context, {'id': id})
            email = config.get('ckan.comments.email', False)
            if email:
                message = 'A comment on the dataset "' + dataset_name + '" has been flagged as offensive / needing moderation. Please visit ' + h.url_for('/moderation/comments') + ' to approve or delete this comment'
                mailer.mail_recipient('Site Administrator', config.get('ckan.comments.admin', 'root@localhost'), 'Dataset Comment Flagged for Moderation',
                                      message)
        except Exception, ee:
            abort(403)

        # Flag the package
        h.flash_notice("Thank you for flagging the comment as inappropriate. It has been marked for moderation.")
        h.redirect_to(str('/dataset/%s' % (c.pkg.name,)))

    def approve(self, id):
        context = {'model': model, 'user': c.user}
        try:
            check_access('comment_update', context, {'id': id})
            get_action('comment_update_approve')(context, {'id': id})
        except Exception, ee:
            abort(403)

        # Flag the package
        h.flash_notice("Comment Approved.")
        h.redirect_to('/moderation/comments')

    def delete(self, id):
        context = {'model': model, 'user': c.user}

        try:
            get_action('comment_update_moderation')(context, {'id': id})
        except Exception, ee:
            abort(403)

        # Flag the package
        h.flash_notice("Comment Deleted.")
        h.redirect_to('/moderation/comments')

    def _get_org_full(self,id):
        try:
            return tk.get_action('organization_show')({'include_datasets': False},{'id': id})
        except tk.ObjectNotFound:
            return None

    def _add_or_reply(self, dataset_name):
        """
        Allows the user to add a comment to an existing dataset
        """
        context = {'model': model, 'user': c.user}

        # Auth check to make sure the user can see this package
        ctx = context
        ctx['id'] = dataset_name
        check_access('package_show', ctx, {'id': dataset_name})

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
                email = config.get('ckan.comments.email', False)
                if email:
                    message = 'There is a new comment on the dataset "' + c.pkg.title + '" \nSubject: ' + res['subject'] + '\n\n' + res[
                        'content']
                    mailer.mail_recipient('Site Administrator', config.get('ckan.comments.admin', 'root@localhost'), 'Dataset Comment',
                                          message)

                    org_full = self._get_org_full(c.pkg_dict['organization']['id'])
                    org_email = h.get_pkg_dict_extra(org_full,'email')
                    if org_email:
                        mailer.mail_recipient('Organisation Administrator', org_email, 'Dataset Comment', message)
                    if 'contact_point' in c.pkg_dict and (not org_email or c.pkg_dict['contact_point'] != org_email):
                        mailer.mail_recipient('Dataset Contact Point', c.pkg_dict['contact_point'], 'Dataset Comment', message)
                h.redirect_to(str('/dataset/%s#comment_%s' % (c.pkg.name, res['id'])))

        vars = {'errors': errors}

        # TODO: Check if user is in BlockedUsers, if so discard any input
        c.form = render('comments/create_form.html', extra_vars=vars)

        return render('comments/create.html')

