from nose.tools import assert_raises
from pylons import config

import ckan.model as model
from ckan.logic import get_action, NotAuthorized

import ckanext.comments.tests.test_data as test_data

class TestCommentThread(object):

    @classmethod
    def setup_class(cls):
        model.repo.new_revision()
        test_data.create()

    @classmethod
    def teardown_class(cls):
        test_data.cleanup()
        model.repo.rebuild_db()

    def test_comment_create_basic(self):
        thread = self._create_valid('/dataset/create_test')
        assert len(thread['comments']) == 1, "Missing top level comment"
        assert len(thread['comments'][0]['comments']) == 1, "Missing child comment"

    def test_comment_delete_valid(self):
        thread = self._create_valid('/dataset/delete_test')

        c_upper_id = thread['comments'][0]['id']
        c_id = thread['comments'][0]['comments'][0]['id']

        # Process a leaf comment
        ctx = { 'model': model, 'session': model.Session,
                'user': test_data.site_user() }
        try:
            res = get_action('comment_delete')(ctx, { 'id': c_id })
        except NotAuthorized:
            assert False, "Should allow user to delete comment"

        try:
            res = get_action('comment_show')(ctx, { 'id': c_id })
        except NotAuthorized:
            assert False, "Should allow user to view comment"
        assert res['state'] == 'deleted', "Comment does not have deleted state"

        # Try a comment that has children
        try:
            res = get_action('comment_delete')(ctx, { 'id': c_upper_id })
        except NotAuthorized:
            assert False, "Should allow user to delete comment"

        try:
            res = get_action('comment_show')(ctx, { 'id': c_upper_id })
        except NotAuthorized:
            assert False, "Should allow user to view comment"

        assert res['content'] == config.get('ckan.comments.deleted.text', 'This message was deleted'),\
            "Comment did not have text set correctly, it has children"


    def _create_valid(self, url):
        ctx = { 'model': model, 'session': model.Session,
                'user': test_data.site_user() }
        data = {
            'url': url,
            'parent_id': '',
            'comment': 'A comment'
        }
        try:
            res = get_action('comment_create')(ctx, data)
        except NotAuthorized:
            assert False, "Should allow user to create valid comment"

        data = {
            'url': url,
            'parent_id': res['id'],
            'comment': 'Another comment'
        }

        try:
            res = get_action('comment_create')(ctx, data)
        except NotAuthorized:
            assert False, "Should allow user to create valid comment"

        return get_action('thread_show')({'model':model, 'user':''}, {'id': res['thread_id']})


    def test_comment_create_fail(self):
        pass