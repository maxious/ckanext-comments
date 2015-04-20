```
This extension is a work in progress
```
# ckanext-comments

This [CKAN](http://ckan.org) extension allows you to add comments to
various things in CKAN (datasets, related items etc)so that users can,
well, comment on things.

## Installation
Set up this extension's database tables using a paster command. (Ensure your CKAN pyenv is still activated, run the command from ``src/ckanext-comments``, alter the ``--config`` option to point to your site config file)::

    $ paster initdb --config=../ckan/development.ini
## Configuration

ckanext-comments has several configuration options that should be set to allow for your required behaviour
    # comment administrator to get emails
    ckan.comments.admin = admin@example.com
    # Whether comments should be threaded or not (default: false)
    ckan.comments.threaded = true/false

    # Whether, only a user's first comment must be moderated  (default: true)
    # otherwise ALL comments are moderated.
    ckan.comments.moderation.first_only = true/false

    # Text for comments that have children and are deleted
    ckan.comments.deleted.text = This comment has been deleted

    # For spam checking to work, the following two fields must be provided
    mollom.public.key = The Mollom public key
    mollom.private.key = The Mollom private key.


## Testing
To run the tests you should run the following command in the ckanext-comments directory (or use --plugin=comments).

    nosetests --ckan --reset-db --with-pylons=test-core.ini ckanext.comments




## TODO

 * Moderation queue
