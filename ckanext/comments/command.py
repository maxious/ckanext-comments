import csv
import datetime
import logging
import os
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


class XMLImport(CkanCommand):
    """
    Imports data from the provided XML into the comment tables.

    XML Generated from:
        SELECT R.id, R.parent,
               D.name "dataset_name",
               R.status,
               R.entity_id,
               U.name "username",
               CS.field_reply_subject_value "subject",
               CF.field_reply_comment_value "comment",
               R.created "timestamp"
        FROM field_revision_field_reply_comment as CF
        INNER JOIN reply as R
            ON R.id = CF.entity_id
        INNER JOIN field_revision_field_reply_subject as CS
            ON CS.entity_id = CF.entity_id
        INNER JOIN users as U
            ON U.uid = R.uid
        INNER JOIN ckan_dataset as D
            ON D.id = R.entity_id
        WHERE
            R.entity_type = 'ckan_dataset'
        ORDER BY R.id;
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 1
    min_args = 1

    def __init__(self, name):
        super(XMLImport, self).__init__(name)

        # Maps old ids to the newly created CKAN comment id.
        self.old_ids = {}

    def command(self):
        self._load_config()
        self.log = logging.getLogger(__name__)

        import ckan.model as model
        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)

        self.input = self.args[0]
        if not os.path.exists(self.input):
            self.log.error("No such file: %s" % self.input)
            sys.exit(1)

        ctx = {}

        from lxml import etree
        tree = etree.parse(self.input)
        rows = tree.xpath('//row')
        for row in rows:
            self.process_row(row, ctx)

    def process_row(self, row, context):
        # "id","parent","dataset_name","status","entity_id","username","subject","comment","timestamp"
        import ckan.model as model
        import ckan.logic as logic

        obj = {
            'id': int(row[0].text),
            'parent': int(row[1].text),
            'dataset_name': row[2].text,
            'status': int(row[3].text),
            'username': row[5].text,
            'subject': row[6].text,
            'comment': row[7].text,
            'timestamp': int(row[8].text)
        }

        data = self._compose_comment_dict(obj)
        user = self._find_user(obj['username'])
        if user:
            context['user'] = user.name
        else:
            # TODO: Setup an anonymous user.
            context['user'] = self._find_user('rossjones').name

        context['creation_date'] = obj['timestamp']

        res = None
        try:
            res = logic.get_action('comment_create')(context, data)
        except Exception, e:
            self.log.exception(e)

        self.old_ids[obj['id']] = res['id']


    def _find_user(self, name):
        import ckan.model as model
        return model.Session.query(model.User).filter(model.User.fullname==name).first()

    def _find_parent(self, id):
        return self.old_ids.get(id)

    def _compose_comment_dict(self, data):
        d = {
            'url': '/dataset/%s' % data['dataset_name'],
            'comment': data['comment'],
            'subject': data['subject']
        }
        if data['parent'] != 0:
            pid = self._find_parent(data['parent'])
            if pid:
                d['parent_id'] = pid

        return d
