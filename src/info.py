import json

import requests

from template_tools.src.request import request
from template_tools.src.urls import info_url, \
    login_url, \
    data_list_url, \
    template_url, \
    team_url


def get_template_id_by_template_name(team_name, template_name):
    team_id = get_team_id_by_team_name(team_name)
    data = {
        'name': "",
        'pageNo': 1,
        'pageSize': 200,
        'teamId': team_id,
    }
    rsp = request(template_url, 'post', json=data)
    records = rsp.get('data', {}).get('records', [])
    for record in records:
        if record['templateName'] == template_name:
            return record['templateId'], record['templateNowEditionId']
    raise Exception("Cannot found template in template list")


def get_team_id_by_team_name(team_name):
    data = {
        'companyName': "",
        'createTimeFrom': "",
        'createTimeTo': "",
        'pageNo': 1,
        'pageSize': 200,
        'teamLeaderName': "",
        'teamName': "",
    }
    rsp = request(team_url, 'post', json=data)
    records = rsp.get('data', {}).get('records', [])
    for record in records:
        if record['teamName'] == team_name:
            return record['teamId']
    raise Exception("Cannot found teamId in team list")


def get_all_data(team_name, template_name, num=9999999, filter_callback=None):
    """get all data json of template
    Args:
        :param team_name: 团队名称
        :param template_name:  模板名称
    """
    team_id = get_team_id_by_team_name(team_name)
    data = {
        "pageNo": 1,
        "pageSize": num,
        "teamId": team_id,
        "templateName": template_name
    }
    rsp = request(data_list_url, 'post', json=data)
    data = rsp.get('data', {}).get('records', [])
    if filter_callback:
        data = filter_callback(data)
    return data


def get_records_num(team_name, template_name):
    """ get records' number of template
    Returns:
        num: records' number of template
    """
    team_id = get_team_id_by_team_name(team_name)
    template_id, _ = get_template_id_by_template_name(
        team_name, template_name)
    data = {
        'teamId': team_id,
        'templateId': template_id
    }
    rsp = request(info_url, 'post', json=data)
    try:
        num = rsp['data']['dataRecords']
        return num
    except KeyError:
        raise Exception("Cannot get records number")
