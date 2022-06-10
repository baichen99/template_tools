import os
import sys
import json
from http.cookies import SimpleCookie

from .request import request
from .urls import delete_url
from .upload import get_all_data


def delete_all(team_id, template_name, token):
    '''delete all data of template'''
    records = get_all_data(template_name, team_id, token).get('records', [])
    all_id = [record['dataId'] for record in records]
    for id_ in all_id:
        data = {
            'dataId': id_
        }
        rsp = request(delete_url, 'post', data, token)
        if rsp.status_code != 200:
            print(rsp.text)

if __name__ == '__main__':
    token = ''
    delete_all(template_name='吸波材料', team_id=14, token=token)