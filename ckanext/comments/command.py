import collections
import logging
import datetime
import os
import re
import time
import sys

from .model import init_tables

from pylons import config
from ckan.lib.cli import CkanCommand


class InitDBCommand(CkanCommand):
    """
    Initialises the database with the required tables

    Connects to the CKAN database and creates the comment
    and thread tables ready for use.
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def __init__(self, name):
        super(InitDBCommand, self).__init__(name)

    def command(self):
        self._load_config()
        log = logging.getLogger(__name__)

        import ckan.model as model
        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)

        import ckanext.comments.model as cmodel
        cmodel.init_tables()
        log.debug("DB tables are setup")
