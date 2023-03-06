import os
import re
import keyword
from http.cookies import SimpleCookie

# check json key in same level is unique
def check_json_keys_unique(json_obj, path=[]):
    if 'name' in json_obj:
        path.append(json_obj['name'])
    if not isinstance(json_obj, dict):
        return True
    children = json_obj.get('children', [])
    check_fields = ['name', '_id']

    for field in check_fields:
        if field not in json_obj:
            raise ValueError(f"Missing key '{field}' at {path}")
        else:
            field_arr = []
            for child in children:
                if field in child and child[field] not in field_arr:
                    field_arr.append(child[field])
                elif child[field] in field_arr:
                    raise ValueError(f"Duplicate value for key '{field}' at {path + [child['name']]}")
    
    if len(children) > 0:
        for i, child in enumerate(children):
            if not check_json_keys_unique(child, path=path):
                return False
            else:
                return True

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

def test_check_json_keys_unique():
    json_data = {
        "_id": "1",
        "name": "parent1",
        "type": "container",
        "children": [
            {
                "_id": "2",
                "name": "child1",
                "type": "value-with-unit",
                "unit": "m"
            },
            {
                "_id": "2",
                "name": "child2",
                "type": "value-with-unit",
                "unit": "kg"
            }
        ]
    }
    try:
        check_json_keys_unique(json_data)
    except ValueError as e:
        print(e)


# test_check_json_keys_unique()