import re
import os
import time
import json
from pygtrans import Translate, Null
import xmindparser
from template_tools.src.utils import make_python_identifier
import uuid
from .utils import check_json_key_unique


client = Translate()

# ------------ create a node ------------

def get_id():
    # make sure id is unique and id is a num
    return str(uuid.uuid4()).replace('-', '')[:16]

def getNodeDesc(node):
    """get key, name(zhCN), name(enUS) of node
    """
    title = node.get('title')
    if title.startswith('file:') or title.startswith('table:') or title.startswith('array:'):
        idx = title.index(':')
        title = title[idx+1:]
    en, name = None, None
    # custom key support
    if '[' in title and ']' in title:
        zh = re.findall(r'^(.*?)[\{\[]', title)[0]
        name = re.findall(r'\[(.*?)\]', title)[0]
    # custom en suport
    elif '{' in title and '}' in title:
        zh = re.findall(r'^(.*?)[\{\[]', title)[0]
        en = re.findall(r'\{(.*?)\}', title)[0]
    else:
        zh = title
    if not en:
        en = zh2en(zh)
    if not name:
        name = escape(en)
    return name, zh, en


def createValueNode(node):
    name, zh, en = getNodeDesc(node)
    return {
        "_id": get_id(),
        "name": name,
        "type": "uncheck-stringtype",
        "typename": "字符型",
        "default": "",
        "fixed": "",
        "required": "false",
        "childrenVisible": "true",
        "enUS": en,
        "zhCN": zh,
        "children": []
    }


def createFileNode(node):
    name, zh, en = getNodeDesc(node)
    return {
        "_id": get_id(),
        "name": name,
        "type": "file-list",
        "typename": "文件型",
        "default": "",
        "fixed": "",
        "required": "false",
        "childrenVisible": "true",
        "enUS": en,
        "zhCN": zh,
        "children": []
    }


def createUnitValueNode(node):
    name, zh, en = getNodeDesc(node)

    unit = node.get('topics')[0].get('title')
    unit = unit[len('unit:'):]
    name, zh, en = getNodeDesc(node)

    return {
        "_id": get_id(),
        "name": name,
        "type": "value-with-unit",
        "typename": "带单位数值",
        "default": "",
        "fixed": "",
        "required": "false",
        "childrenVisible": "true",
        "children": [],
        "enUS": en,
        "zhCN": zh,
        "unit": unit,
    }


def createTableNode(node):
    name, zh, en = getNodeDesc(node)
    children = []
    for child in node.get('topics'):
        if checkValueFiled(child):
            children.append(createValueNode(child))
        elif checkUnitValueFiled(child):
            children.append(createUnitValueNode(child))
        elif checkFileFiled(child):
            children.append(createFileNode(child))
    return {
        "_id": get_id(),
        "name": name,
        "type": "table",
        "typename": "表格型",
        "default": "",
        "fixed": "",
        "required": "false",
        "childrenVisible": "true",
        "enUS": en,
        "zhCN": zh,
        "children": children
    }


def createArrayNode(node):
    name, zh, en = getNodeDesc(node)
    children = []
    for child in node.get('topics'):
        if checkValueFiled(child):
            children.append(createValueNode(child))
        elif checkUnitValueFiled(child):
            children.append(createUnitValueNode(child))
        elif checkFileFiled(child):
            children.append(createFileNode(child))
        elif checkTable(child):
            children.append(createTableNode(child))
        elif checkArray(child):
            children.append(createArrayNode(child))
        elif checkContainer(child):
            children.append(createContainerNode(child))
    return {
        "_id": get_id(),
        "name": name,
        "type": "array",
        "typename": "数组型",
        "default": "",
        "fixed": "",
        "required": False,
        "childrenVisible": True,
        "enUS": en,
        "zhCN": zh,
        "children": children
    }


def createContainerNode(node):
    name, zh, en = getNodeDesc(node)
    children = []
    for child in node.get('topics'):
        if checkValueFiled(child):
            children.append(createValueNode(child))
        elif checkUnitValueFiled(child):
            children.append(createUnitValueNode(child))
        elif checkFileFiled(child):
            children.append(createFileNode(child))
        elif checkTable(child):
            children.append(createTableNode(child))
        elif checkArray(child):
            children.append(createArrayNode(child))
        elif checkContainer(child):
            children.append(createContainerNode(child))
    return {
        "_id": get_id(),
        "name": name,
        "type": "container",
        "typename": "容器型",
        "default": "",
        "fixed": "",
        "required": "false",
        "childrenVisible": "true",
        "enUS": en,
        "zhCN": zh,
        "children": children
    }
# ------------ checkers ------------


def checkUnitValueFiled(node):
    if node.get('topics') and node.get('topics')[0].get('title').startswith('unit'):
        return True
    return False


def checkFileFiled(node):
    if node.get('title').startswith('file:'):
        return True
    return False


def checkValueFiled(node):
    # 是否为叶子结点/是否有孩子
    # 如果没有孩子, 且不是unit, table, file结点就是叶子结点
    if not node.get('topics') and not any([t in node.get('title') for t in ['unit', 'table', 'file']]):
        return True
    return False


def checkContainer(node):
    # 是否为容器
    if node.get('topics') and not checkUnitValueFiled(node):
        return True
    return False


def checkTable(node):
    # 是否为表格
    if node.get('title').startswith('table:'):
        return True
    return False


def checkArray(node):
    # 是否为数组
    if node.get('title').startswith('array:'):
        return True
    return False


def getChildrenName(node):
    topics = node.get('topics')
    return [topic.get('title') for topic in topics]

# ------ translator ------


def contain_chinese(s):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def escape(s):
    # replace('_', '-')：与前端保持一致
    return make_python_identifier(s)[0].replace('_', '-')


def zh2en(content):
    if not contain_chinese(content):
        return content
    text = client.translate(content, target='en')
    if isinstance(text, Null):
        return None
    else:
        return text.translatedText


def getTemplate(xmind_path, from_json=None, dest='template.json'):
    if not from_json:
        xmindparser.xmind_to_json(xmind_path)
        json_file = os.path.splitext(xmind_path)[0] + '.json'
        data = json.load(open(json_file))[0].get('topic')
    else:
        data = json.load(open(from_json))[0].get('topic')

    with open(dest, 'w', encoding='utf-8') as f:
        out = createContainerNode(data)
        # if check_json_key_unique(out):
        #     print('json key唯一性检查通过')
        out = json.dumps(out, ensure_ascii=False)
        f.write(out)


if __name__ == '__main__':
    getTemplate('example.xmind')
