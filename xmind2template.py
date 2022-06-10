import re
import os
import time
import json
from pygtrans import Translate, Null
import xmindparser
from .utils import make_python_identifier


client = Translate()

# ------------ create a node ------------
def getNodeDesc(node):
    """get key, name(zhCN), name(enUS) of node
    """
    title = node.get('title')
    if title.startswith('file:') and title.startswith('table:'):
        idx = title.index(':')
        title = title[idx+1:]
    if '[' in title and ']' in title:
        zh, name = re.findall(r'(.*?)\[(.*?)\]$', title)[0]
        en = zh2en(zh)
    else:
        zh = title
        en = zh2en(zh)
        name = escape(en)
    return name, zh, en

def createValueNode(node):
    name, zh, en = getNodeDesc(node)
    return {
            "_id": hash(time.time()),
            "name":name,
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
        "_id": hash(time.time()),
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
    return {
            "_id": hash(time.time()),
            "name": name,
            "type": "value-with-unit",
            "typename": "带单位数值",
            "default": "",
            "fixed": "",
            "required": "false",
            "childrenVisible": "true",
            "enUS": en,
            "zhCN": zh,
            "children": [
                {
                    "_id": hash(time.time()),
                    "name": "_value",
                    "type": "uncheck-stringtype",
                    "typename": "字符型",
                    "default": "",
                    "fixed": "",
                    "required": "false",
                    "childrenVisible": "true",
                    "enUS": "_value",
                    "zhCN": "值",
                    "children": []
                },
                {
                    "_id": hash(time.time()),
                    "name": "_unit",
                    "type": "uncheck-stringtype",
                    "typename": "字符型",
                    "default": "",
                    "fixed": unit,
                    "required": "false",
                    "childrenVisible": "true",
                    "enUS": "_unit",
                    "zhCN": "单位",
                    "children": []
                }
            ]
        }

def createTableNode(node):
    name, zh, en = getNodeDesc(node)
    children = []
    for child in node.get('topics'):
        if checkValueFiled(child):
            children.append(createValueNode(child))
        elif checkUnitValueFiled(child):
            children.append(createUnitValueNode(child))
        elif checkFileFiled(node):
            children.append(createFileNode(child))
    return {
            "_id": hash(time.time()),
            "name": name,
            "type": "container",
            "typename": "表格型",
            "default": "",
            "fixed": "",
            "required": "false",
            "childrenVisible": "true",
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
        elif checkContainer(child):
            children.append(createContainerNode(child))
    return {
            "_id": hash(time.time()),
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

def getChildrenName(node):
    topics = node.get('topics')
    return [topic.get('title') for topic in topics]

# ------ translator ------
def escape(s):
    return make_python_identifier(s)[0]

def zh2en(content):
    text = client.translate(content, target='en')
    if isinstance(text, Null):
        return None
    else:
        return text.translatedText

# -------- get levels of xmind -------
def createValueObj(node):
    title = node.get('title')
    return {
        title: []
    }

def createUnitValueObj(node):
    title = node.get('title')
    return {
        title: []
    }

def createContainerObj(node):
    title = node.get('title')
    children = []
    for child in node.get('topics'):
        if checkValueFiled(child):
            children.append(createValueObj(child))
        elif checkUnitValueFiled(child):
            children.append(createUnitValueObj(child))
        elif checkContainer(child):
            children.append(createContainerObj(child))
    return {
        title: children
    }


# # 保存层级关系，方便录入数据
# with open('levels.json', 'w', encoding='utf-8') as f:
#     level = {}
#     out = createContainerObj(data)
#     out = json.dumps(out, ensure_ascii=False)
#     f.write(out)

def getTemplate(xmind_path, dest='template.json'):
    xmindparser.xmind_to_json(xmind_path)
    json_file = os.path.splitext(xmind_path)[0] + '.json'
    data = json.load(open(json_file))[0].get('topic')

    with open(dest, 'w', encoding='utf-8') as f:
        out = createContainerNode(data)
        out = json.dumps(out, ensure_ascii=False)
        f.write(out)

if __name__ == '__main__':
    getTemplate('材料性能.xmind')