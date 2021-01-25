import re

from helpers import file_helper

""" REGEX DESCRIPTION:

    Finds '{{ caller() }}' and replaces them with:
    {{ html_block_one }}, 
    {{ html_block_two }}, 
    {{ ... }}

    => Group 0: full match
    => Group 1: open tag '{{'
    => Group 2: caller
    => Group 3: close tag with '() }}'
"""
def replace_caller_methods(string):

    pattern = r"(\{\{\s*)(caller)(\(\)\s*\}\})"
    words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten' ]

    # Reset counter for every macro partial.
    counter = 0

    # Iterate over matches, so count doesn't go above the max words array index.
    for match in re.finditer(pattern, string):

        # Only do this replace once per found match. So counter gets incremented.
        string = re.sub("caller\(\)", 'data.html_block_' + words[counter], string, 1)

        counter += 1

    return string


""" REGEX DESCRIPTION:

    Find macro start to end tag and everything in between.
    Returns an array with arrays of groups.

    => Group 0: full match, start to end
    => Group 1: macro start tag
    => Group 2: macro close tag
"""
def get_macros_as_strings_from_file_content(file_content):

    return re.findall(
        r"\{\%\s*macro\s*[a-zA-Z]*\s*\(\s*data\s*\)\s*\%\}.*?\{\%\s*endmacro\s*\%\}",
        file_content,
        re.DOTALL
    )

""" REGEX DESCRIPTION:

    Find macro start to end tag and everything in between.
    Returns an array with match objects.

    => Group 0: full match, start to end
    => Group 1: macro start tag
    => Group 2: macro close tag
"""
def get_macros_as_match_objects_from_file_content(file_content):

    return re.finditer(
        r"(\{\%\s*macro\s*[a-zA-Z]*\s*\(\s*data\s*\)\s*\%\}).*?(\{\%\s*endmacro\s*\%\})",
        file_content,
        re.DOTALL
    )

""" REGEX DESCRIPTION:

    Find macro start to end tag and everything in between.
    Returns an array with arrays of groups.

    => TODO; explain groups
"""
def get_from_import_tags_from_file_content(file_content):

    return re.findall(
        r"(\{\%\s*from\s*\'[a-z-.\/]*.*\'\s*import\s*([a-zA-Z]*)\s*\%\})",
        file_content
    )

""" REGEX DESCRIPTION:

    Find macro start to end tag and everything in between.
    Returns an array with arrays of groups.

    => TODO; explain groups
"""
def get_from_import_as_tags_from_file_content(file_content):

    return re.findall(
        r"(\{\%\s*from\s*\'[a-z-.\/]*.*\'\s*import.*as\s*([a-zA-Z]*)\s*%\})",
        file_content
    )

""" REGEX DESCRIPTION:

    Find macro start to end tag and everything in between.
    Returns an array with arrays of groups.

    => TODO; explain groups
"""
def get_import_as_tags_from_file_content(file_content):

    return re.findall(
        r"(\{\%\s*import\s*\'[a-z-.\/]*\'\s*as\s*([a-zA-Z]*)\s*\%\})",
        file_content
    )

""" REGEX DESCRIPTION:

    Removes all comments {# ... #}

    => Group 0: full match
"""
def remove_twig_comments_from_file_content(file_content):

    return re.sub(
        re.compile(r"\{\#.*?\#\}", re.DOTALL),
        '',
        file_content
    )


""" REGEX DESCRIPTION:

    Returns all comments {# ... #}.
    
    => Group 0: full match
"""
def get_twig_comments_from_file_content(file_content):

    return re.findall(
        re.compile(r"\{\#.*?\#\}", re.DOTALL),
        file_content
    )