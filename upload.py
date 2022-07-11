import os
import json
import shutil
import tempfile

import requests

from .request import request
from .urls import base_url, \
    file_upload_url, \
    info_url, \
    add_url, \
    login_url, \
    data_list_url, \
    upload_url, \
    template_url, \
    team_url


def upload_asset(file_obj, token):
    rsp = request(file_upload_url, 'post', token=token, json={'typeCode': 'file'}, files={'file': file_obj})
    try:
        file_id = json.loads(rsp.text)['data']['objectId']
    except Exception as e:
        print(e)
        return None
    return f'/mgd/rest/blob/download/{file_id}'


def upload_xml(file_path, name, team_name, template_name, token):
    team_id = get_team_id_by_team_name(team_name, token)
    _, template_edition_id = get_template_id_by_template_name(team_name, template_name, token)
    with open(file_path, 'r', encoding='utf-8', newline='\r\n') as f:
        s = f.read()
    form = {
        'name': name,
        'templateEditionId': template_edition_id,
        'teamId': team_id,
        'keywords': '',
        'content': s,
        'type': 1
    }
    rsp = request(add_url, 'post', token, json=form)
    return json.loads(rsp.text)


def upload_zip(file_path, name, team_name, template_name, token, compress=False):
    team_id = get_team_id_by_team_name(team_name, token)
    _, template_edition_id = get_template_id_by_template_name(team_name, template_name, token)
    form = {
        'name': name,
        'teamId': team_id,
        'templateEditionId': template_edition_id,
    }
    if compress:
        tmp_dir = tempfile.TemporaryDirectory()

        zip_path = os.path.join(tmp_dir.name, 'data.zip')
        shutil.make_archive(os.path.join(tmp_dir.name, 'data'), 'zip', file_path)
        file_path = zip_path

    rsp = request(upload_url, 'post', token=token, data=form, files={'file': open(file_path, 'rb')})
    return rsp


def get_template_id_by_template_name(team_name, template_name, token):
    team_id = get_team_id_by_team_name(team_name, token)
    data = {
        'name': "",
        'pageNo': 1,
        'pageSize': 200,
        'teamId': team_id,
    }
    rsp = request(template_url, 'post', token, json=data)
    records = json.loads(rsp.text).get('data', {}).get('records', [])
    for record in records:
        if record['templateName'] == template_name:
            return record['templateId'], record['templateNowEditionId']
    return None


def get_team_id_by_team_name(team_name, token):
    data = {
        'companyName': "",
        'createTimeFrom': "",
        'createTimeTo': "",
        'pageNo': 1,
        'pageSize': 200,
        'teamLeaderName': "",
        'teamName': "",
    }
    rsp = request(team_url, 'post', token, json=data)
    records = json.loads(rsp.text).get('data', {}).get('records', [])
    for record in records:
        if record['teamName'] == team_name:
            return record['teamId']
    return 0


def get_all_data(team_name, template_name, token, num=1000):
    """get all data json of template
    Args:
        :param team_name: 团队名称
        :param template_name:  模板名称
    """
    team_id = get_team_id_by_team_name(team_name, token)
    data = {
        "pageNo": 1,
        "pageSize": num,
        "teamId": team_id,
        "templateName": template_name
    }
    rsp = request(data_list_url, 'post', token, json=data)
    data = json.loads(rsp.text).get('data', {})
    return data


def get_token(username, password):
    data = {
        'account': username,
        'password': password
    }
    rsp = requests.post(login_url, json=data)
    token = json.loads(rsp.text)['data']['token']
    return token


def get_records_num(team_name, template_name, token):
    """ get records' number of template
    Returns:
        num: records' number of template
    """
    team_id = get_team_id_by_team_name(team_name, token)
    template_id, _ = get_template_id_by_template_name(team_name, template_name, token)
    data = {
        'teamId': team_id,
        'templateId': template_id
    }
    rsp = request(info_url, 'post', json=data, token=token)
    num = json.loads(rsp.text)['data']['dataRecords']
    return num


if __name__ == '__main__':
    pass
