import ckan.model as model
from ckan.logic import get_action


def create():
    # Create the relevant comment tables and insert some test data
    from ckanext.comments.model import init_tables
    init_tables()




def cleanup():
    # Remove all created comments/threads/blockedusers so that the
    # DB can be torn down.
    from ckanext.comments.model import Comment, CommentThread, CommentBlockedUser

    model.Session.query(CommentBlockedUser).delete()
    model.Session.query(Comment).delete()
    model.Session.query(CommentThread).delete()

    model.Session.commit()

def site_user():
    return get_action('get_site_user')({'model':model,'ignore_auth': True},{})['name']