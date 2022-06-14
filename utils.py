import os
import re
import keyword
import pathlib
import requests
from uuid import uuid4

from http.cookies import SimpleCookie
from xml.etree import ElementTree
from mimetypes import guess_extension

from .request import request

def cookieStr_to_dict(cookie_str):
    cookie = SimpleCookie()
    cookie.load(cookie_str)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies


def make_python_identifier(string, namespace=None, reserved_words=None,
                           convert='drop', handle='force'):
    """
    Takes an arbitrary string and creates a valid Python identifier.
    If the python identifier created is already in the namespace,
    or if the identifier is a reserved word in the reserved_words
    list, or is a python default reserved word,
    adds _1, or if _1 is in the namespace, _2, etc.
    Parameters
    ----------
    string : <basestring>
        The text to be converted into a valid python identifier
    namespace : <dictionary>
        Map of existing translations into python safe identifiers.
        This is to ensure that two strings are not translated into
        the same python identifier
    reserved_words : <list of strings>
        List of words that are reserved (because they have other meanings
        in this particular program, such as also being the names of
        libraries, etc.
    convert : <string>
        Tells the function what to do with characters that are not
        valid in python identifiers
        - 'hex' implies that they will be converted to their hexidecimal
                representation. This is handy if you have variables that
                have a lot of reserved characters
        - 'drop' implies that they will just be dropped altogether
    handle : <string>
        Tells the function how to deal with namespace conflicts
        - 'force' will create a representation which is not in conflict
                  by appending _n to the resulting variable where n is
                  the lowest number necessary to avoid a conflict
        - 'throw' will raise an exception
    Returns
    -------
    identifier : <string>
        A vaild python identifier based on the input string
    namespace : <dictionary>
        An updated map of the translations of words to python identifiers,
        including the passed in 'string'.
    Examples
    --------
    >>> make_python_identifier('Capital')
    ('capital', {'Capital': 'capital'})
    >>> make_python_identifier('multiple words')
    ('multiple_words', {'multiple words': 'multiple_words'})
    >>> make_python_identifier('multiple     spaces')
    ('multiple_spaces', {'multiple     spaces': 'multiple_spaces'})
    When the name is a python keyword, add '_1' to differentiate it
    >>> make_python_identifier('for')
    ('for_1', {'for': 'for_1'})
    Remove leading and trailing whitespace
    >>> make_python_identifier('  whitespace  ')
    ('whitespace', {'  whitespace  ': 'whitespace'})
    Remove most special characters outright:
    >>> make_python_identifier('H@t tr!ck')
    ('ht_trck', {'H@t tr!ck': 'ht_trck'})
    Replace special characters with their hex representations
    >>> make_python_identifier('H@t tr!ck', convert='hex')
    ('h40t_tr21ck', {'H@t tr!ck': 'h40t_tr21ck'})
    remove leading digits
    >>> make_python_identifier('123abc')
    ('abc', {'123abc': 'abc'})
    namespace conflicts
    >>> make_python_identifier('Variable$', namespace={'Variable@':'variable'})
    ('variable_1', {'Variable@': 'variable', 'Variable$': 'variable_1'})
    >>> make_python_identifier('Variable$', namespace={'Variable@':'variable', 'Variable%':'variable_1'})
    ('variable_2', {'Variable@': 'variable', 'Variable%': 'variable_1', 'Variable$': 'variable_2'})
    throw exception instead
    >>> make_python_identifier('Variable$', namespace={'Variable@':'variable'}, handle='throw')
    Traceback (most recent call last):
     ...
    NameError: variable already exists in namespace or is a reserved word
    References
    ----------
    Identifiers must follow the convention outlined here:
        https://docs.python.org/2/reference/lexical_analysis.html#identifiers
    """

    if namespace is None:
        namespace = {}

    if reserved_words is None:
        reserved_words = []

    # create a working copy (and make it lowercase, while we're at it)
    # s = string.lower()

    # remove leading and trailing whitespace
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

def getFilename(headers):
    d = headers.get('content-disposition', '')
    fname = re.findall("filename=(.+)", d)
    if fname:
        return fname[0]
    return

def download(url, token, save_path=None):
    rsp = request(url, 'get', token=token)
    if save_path:
        with open(save_path, 'wb') as f:
            f.write(r.content)
    else:
        return r.content

def getFilenameAndSave(url, output_dir, filename=None):
    # 下载附件并保存到文件夹，返回存储的文件名
    r = requests.get(url)
    if not filename:
        filename = getfilename(r.headers)
        if not filename:
            ext = pathlib.Path(filename).suffix or guess_extension(
                r.headers['content-type'].partition(';')[0].strip())
            filename = f'{str(uuid4())}{ext}'
    dest_path = os.path.join(output_dir, filename)
    with open(dest_path, 'wb') as f:
        f.write(r.content)
    return filename


def parse_xml(file_path):
    tree = ElementTree.parse(file_path)
    return tree


def replaceUrlWithImport(output_dir, tree):
    # 遍历所有node，将url对应的资源下载并保存，然后替换原来的url为文件路径
    root = tree.getroot()
    all_nodes = []
    for elem in root.iter():
        all_nodes.append(elem)
    for node in all_nodes:
        # 单独处理文件标签
        if node.tag == 'file':
            filename = ''
            download_url = ''
            for child in node:
                # 获取附件文件名
                if child.tag == 'name' and child.text:
                    filename = child.text
                # 获取附件url
                if child.tag == 'url' and child.text:
                    if child.text.startswith('/'):
                        download_url = 'http://matdata.shu.edu.cn' + child.text
                    elif child.text.startswith('http'):
                        download_url = child.text
                    elif child.text.startswith('import:'):
                        break
                    elif child.text == '':
                        break
                    else:
                        download_url = 'http://' + child.text
                    child.text = f'import:{filename}'
        #   print(download_url)
            if download_url == '' or download_url.startswith('import:'):
                continue
            getFilenameAndSave(download_url, output_dir, filename)
    return tree
