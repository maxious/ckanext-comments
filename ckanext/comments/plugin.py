import logging
import ckan.lib.helpers as h
import ckan.plugins as p
from ckan.config.routing import SubMapper
from ckan.plugins import implements, toolkit

log = logging.getLogger('ckanext.comments')

class CommentsPlugin(p.SingletonPlugin):
    implements(p.IConfigurer, inherit=True)
    implements(p.ITemplateHelpers, inherit=True)
    implements(p.IRoutes, inherit=True)
    implements(p.IAuthFunctions, inherit=True)
    implements(p.IActions, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        """
        A dictionary of extra helpers that will be available to provide
        info to templates.
        """
        return {
            'comments_installed': lambda: True,
        }

    def get_actions(self):
        import ckanext.comments.logic.action as actions
        return {
            "comment_create": actions.create.comment_create,
            "comment_delete": actions.delete.comment_delete,
            "comment_show": actions.get.comment_show,
            "comment_update": actions.update.comment_update,
            "thread_show": actions.get.thread_show,
            "moderation_queue_show": actions.get.moderation_queue_show,
            "moderation_queue_update": actions.update.moderation_queue_update,
        }

    def get_auth_functions(self):
        import ckanext.comments.logic.auth as auths
        return {
            "comment_create": auths.create.comment_create,
            "comment_delete": auths.delete.comment_delete,
            "comment_show": auths.get.comment_show,
            "comment_update": auths.update.comment_update,
            "thread_show": auths.get.thread_show,
            "moderation_queue_show": auths.get.moderation_queue_show,
            "moderation_queue_update": auths.update.moderation_queue_update,
        }

    def before_map(self, map):
        """
        Add the API endpoints, we only want to use APIs. This should really be in
        logic so accessible through the normal APIs.
        """

        return map

    def after_map(self, map):
        return map
