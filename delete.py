import os
import sys
import json
import requests
from http.cookies import SimpleCookie

from request import request


def get_all_data(url, template_name, team_id, token, num=1000):
    '''get all data json of template
    Args:
        url:            url of get all data api, e.g. 'http://xxx/mgd/api/data/list'
        template_name:  e.g. 吸波材料
    '''
    data = {
        "pageNo": 1,
        "pageSize": num,
        "teamId": team_id,
        "templateName": template_name
    }
    rsp = request(url, 'post', data, token)
    data = json.loads(rsp.text).get('data', {})
    return data

def delete_all(url, team_id, template_name, token):
    '''delete all data of template
    Args:
        url: url of get all data api, e.g. 'http://xxx/mgd/api/data/delete'
    '''
    records = get_all_data(template_name, team_id, token).get('records', [])
    all_id = [record['dataId'] for record in records]
    for id_ in all_id:
        data = {
            'dataId': id_
        }
        rsp = request(url, 'post', data, token)
        if rsp.status_code != 200:
            print(rsp.text)

if __name__ == '__main__':
    token = ''
    delete_all(template_name='吸波材料', team_id=14, token=token)