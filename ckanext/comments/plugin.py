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

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        """
        A dictionary of extra helpers that will be available to provide
        ga report info to templates.
        """
        return {
        #    'linkfinder_installed': lambda: True,
        }


    def before_map(self, map):
        """
        Make "/data" the homepage.
        """
        api_controller = 'ckanext.comments.controllers.api:CommentApiController'
        with SubMapper(map, controller=api_controller) as m:
            m.connect('/comments/thread/{object_type}/{object_id}', action='thread')

        return map

    def after_map(self, map):
        return map