import os
import json
import shutil

from .request import request

from .urls import file_upload_url, info_url, add_url, login_url, data_list_url


def upload_asset(file_obj, token):
    rsp = request(file_upload_url, 'post', token=token, json={'typeCode': 'file'}, files={'file': file_obj})
    try:
        file_id = json.loads(rsp.text)['data']['objectId']
    except Exception as e:
        print(e)
        return None
    return f'/mgd/rest/blob/download/{file_id}'

def upload_xml(file_path, name, template_id, team_id, token):
    with open(file_path, 'r', encoding='utf-8') as f:
        s = f.read()
    form = {
        'name': name,
        'templateEditionId': template_id,
        'teamId': team_id,
        'keywords': '',
        'content': s,
        'type': 1
    }
    rsp = request(add_url, 'post', json=form)
    return rsp

def get_all_data(template_name, team_id, token, num=1000):
    '''get all data json of template
    Args:
        template_name:  e.g. 吸波材料
    '''
    data = {
        "pageNo": 1,
        "pageSize": num,
        "teamId": team_id,
        "templateName": template_name
    }
    rsp = request(data_list_url, 'post', data, token)
    data = json.loads(rsp.text).get('data', {})
    return data

def get_token(username, password):
    data = {
        'account': username,
        'password': password
    }
    rsp = request(login_url, 'post', json=data)
    token = json.loads(rsp.text)['data']['token']
    return token

def get_records_num(team_id, template_id, token):
    ''' get records' number of template
    Returns:
        num: records' number of template
    '''
    data = {
        'teamId': team_id,
        'templateId': template_id
    }
    rsp = request(info_url, 'post', json=data, token=token)
    num = json.loads(rsp.text)['data']['dataRecords']
    return num

if __name__ == '__main__':
    pass
