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
            "thread_create": actions.create.thread_create,
            "comment_delete": actions.delete.comment_delete,
            "thread_delete": actions.delete.thread_delete,
            "comment_show": actions.get.comment_show,
            "thread_show": actions.get.thread_show,
            "comment_list": actions.get.comment_list,
            "comment_update": actions.update.comment_update,
            "thread_update": actions.update.thread_update,
        }

    def get_auth_functions(self):
        import ckanext.comments.logic.action as auths
        return {
            "comment_create": auths.create.comment_create,
            "thread_create": auths.create.thread_create,
            "comment_delete": auths.delete.comment_delete,
            "thread_delete": auths.delete.thread_delete,
            "comment_show": auths.get.comment_show,
            "thread_show": auths.get.thread_show,
            "comment_list": auths.get.comment_list,
            "comment_update": auths.update.comment_update,
            "thread_update": auths.update.thread_update,
        }

    def before_map(self, map):
        """
        Add the API endpoints, we only want to use APIs. This should really be in
        logic so accessible through the normal APIs.
        """
        api_controller = 'ckanext.comments.controllers.api:CommentApiController'
        with SubMapper(map, controller=api_controller) as m:
            m.connect('/comments/thread/{object_type}/{object_id}', action='thread')

        return map

    def after_map(self, map):
        return map
