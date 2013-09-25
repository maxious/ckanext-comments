# ckanext-comments

This [CKAN](http://ckan.org) extension allows you to add comments to
various things in CKAN (datasets, related items etc)so that users can,
well, comment on things.

## Installation


## Configuration

ckanext-comments has several configuration options that should be set to allow for your required behaviour

    # Whether comments should be threaded or not (default: false)
    ckan.comments.threaded = true/false

    # Whether comments must be moderated or not (default: true)
    ckan.comments.moderation = true/false

    # Whether, when moderation is on, only a user's first comment
    # must be moderated  (default: true)
    ckan.comments.moderation.first_only = true/false
    
 

## Testing
To run the tests you should run the following command in the ckanext-comments directory (or use --plugin=comments).

    nosetests
 
 
 
 