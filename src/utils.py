import os
import re
import keyword
from http.cookies import SimpleCookie


def cookieStr_to_dict(cookie_str):
    cookie = SimpleCookie()
    cookie.load(cookie_str)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies


def make_python_identifier(string, namespace=None, reserved_words=None,
                           convert='drop', handle='force'):
    """convert a string to a valid python identifier
    """

    if namespace is None:
        namespace = {}

    if reserved_words is None:
        reserved_words = []

    # create a working copy (and make it lowercase, while we're at it)
    # s = string.lower()

    # remove leading and trailing whitespace
    if not string:
        string = ''
    s = string.strip()

    # Make spaces into underscores
    s = re.sub('[\\s\\t\\n]+', '_', s)

    if convert == 'hex':
        # Convert invalid characters to hex
        s = ''.join([c.encode("hex") if re.findall(
            '[^0-9a-zA-Z_]', c) else c for c in s])

    elif convert == 'drop':
        # Remove invalid characters
        s = re.sub('[^0-9a-zA-Z_]', '', s)

    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)

    # Check that the string is not a python identifier
    while (s in keyword.kwlist or
           s in namespace.values() or
           s in reserved_words):
        if handle == 'throw':
            raise NameError(
                s + ' already exists in namespace or is a reserved word')
        if handle == 'force':
            if re.match(".*?_\d+$", s):
                i = re.match(".*?_(\d+)$", s).groups()[0]
                s = s.strip('_'+i) + '_'+str(int(i)+1)
            else:
                s += '_1'

    namespace[string] = s

    return s, namespace
