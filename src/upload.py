import os
import json
import shutil
import tempfile
from glob import glob

import requests
from tqdm import tqdm

from template_tools.src.request import request
from template_tools.src.urls import file_upload_url, \
    add_url, \
    upload_url
from template_tools.src.info import get_records_num, get_team_id_by_team_name, get_template_id_by_template_name


def upload_asset(file_obj):
    rsp = request(file_upload_url, 'post', json={
                  'typeCode': 'file'}, files={'file': file_obj})
    try:
        file_id = json.loads(rsp.text)['data']['objectId']
    except KeyError as e:
        raise Exception("upload asset failed: ", str(e))
    return f'/mgd/rest/blob/download/{file_id}'


def upload_job(type='xml', team_name='', template_name='', file_path='', compress=False):
    idx = get_records_num(team_name, template_name) + 1
    if type == 'xml':
        for file in tqdm(glob(os.path.join(file_path, '*.xml'))):
          try:
            upload_xml(file, f'{template_name}_{idx}',
                       team_name, template_name)
            idx += 1
          except Exception as e:
            print(e)
    elif type == 'zip':
        for folder in tqdm(glob(os.path.join(file_path, '*'))):
            if not os.path.isdir(folder):
                continue
            try:
                upload_zip(folder, f'{template_name}_{idx}',
                           team_name, template_name, compress)
                idx += 1
            except Exception as e:
                print(e)
    else:
        raise Exception('type error')


def upload_xml(file_path, name, team_name, template_name):
    team_id = get_team_id_by_team_name(team_name)
    _, template_edition_id = get_template_id_by_template_name(
        team_name, template_name)
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
    rsp = request(add_url, 'post', json=form)
    return rsp


def upload_zip(file_path, name, team_name, template_name, compress=False):
    team_id = get_team_id_by_team_name(team_name)
    _, template_edition_id = get_template_id_by_template_name(
        team_name, template_name)
    form = {
        'name': name,
        'teamId': team_id,
        'templateEditionId': template_edition_id,
    }
    if compress:
        tmp_dir = tempfile.TemporaryDirectory()

        zip_path = os.path.join(tmp_dir.name, 'data.zip')
        shutil.make_archive(os.path.join(
            tmp_dir.name, 'data'), 'zip', file_path)
        file_path = zip_path

    rsp = request(upload_url, 'post', data=form,
                  files={'file': open(file_path, 'rb')})
    return rsp


if __name__ == '__main__':
    pass
