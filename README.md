# ckanext-comments

This [CKAN](http://ckan.org) extension allows you to add comments to
various things in CKAN (datasets, related items etc)so that users can,
well, comment on things.

## Installation


## Configuration

ckanext-comments has several configuration options that should be set to allow for your required behaviour

    # Whether comments should be threaded or not (default: false)
    ckan.comments.threaded = true/false

    # Whether, only a user's first comment must be moderated  (default: true)
    # otherwise ALL comments are moderated.
    ckan.comments.moderation.first_only = true/false
    
    # Text for comments that have children and are deleted
    ckan.comments.deleted.text = This comment has been deleted
    
 

## Testing
To run the tests you should run the following command in the ckanext-comments directory (or use --plugin=comments).

    nosetests --ckan --reset-db --with-pylons=test-core.ini ckanext.comments
 
 
 
## TODO

 * Spam checking via mollom/akismet
 * Moderation queue
 * ~~~Move all of the logic into the logic layer~~~ 
 * Make sure any provided JS makes the right API calls and handles threads properly
 