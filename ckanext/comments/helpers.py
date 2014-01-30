


def get_comments_dict(url):
    import ckan.model as model
    from ckan.logic import get_action

    return get_action('thread_show')({'model': model}, {'url': url})
