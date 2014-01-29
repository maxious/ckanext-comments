from lxml.html.clean import Cleaner

ALLOWED_TAGS = [
    "a", "em", "strong", "cite", "code", "ul", "ol", "li", "p", "blockquote"
]

def clean_input(comment):
    cleaner = Cleaner(add_nofollow=True, allow_tags=ALLOWED_TAGS,
                      remove_unknown_tags=False)
    return cleaner.clean_html(comment)

def format_comment(comment):
    # Formats the comment text to be more useful. Currently
    # does nothing.
    return comment