from nose.tools import assert_raises

import ckan.model as model
import ckanext.comments.tests.test_data as test_data
from ckan.logic import get_action, NotAuthorized

class TestCommentThreadCreate(object):

    @classmethod
    def setup_class(cls):
        model.repo.new_revision()
        test_data.create()

    @classmethod
    def teardown_class(cls):
        test_data.cleanup()
        model.repo.rebuild_db()

    def test_comment_create_basic(self):
        ctx = { 'model': model, 'session': model.Session,
                'user': test_data.site_user() }
        data = {
            'url': '/dataset/test',
            'parent_id': '',
            'comment': 'A comment'
        }
        try:
            res = get_action('comment_create')(ctx, data)
        except NotAuthorized:
            assert False, "Should allow user to create valid comment"

        data = {
            'url': '/dataset/test',
            'parent_id': res['id'],
            'comment': 'Another comment'
        }

        try:
            res = get_action('comment_create')(ctx, data)
        except NotAuthorized:
            assert False, "Should allow user to create valid comment"

        thread = get_action('thread_show')({'model':model, 'user':''}, {'id': res['thread_id']})

        assert len(thread['comments']) == 1, "Missing top level comment"
        assert len(thread['comments'][0]['comments']) == 1, "Missing child comment"


    def test_comment_create_fail(self):
        pass