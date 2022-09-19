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
from concurrent.futures import ThreadPoolExecutor, as_completed


def upload_asset(file_obj):
    rsp = request(file_upload_url, 'post', json={
                  'typeCode': 'file'}, files={'file': file_obj})
    try:
        file_id = json.loads(rsp.text)['data']['objectId']
    except KeyError as e:
        raise Exception("upload asset failed: ", str(e))
    return f'/mgd/rest/blob/download/{file_id}'


def upload_job(type='xml', team_name='', template_name='', file_paths='', prefix='', compress=True, max_workers=10):
    idx = get_records_num(team_name, template_name) + 1
    prefix = prefix or template_name
    if type == 'xml':
        files = []
        for file_path in file_paths:
            files.extend(glob(os.path.join(file_path, '*.xml')))
        names = [f'{prefix}_{i}' for i in range(idx, idx+len(files))]

        with tqdm(files) as pbar:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(upload_xml,
                                           files[i], names[i], team_name, template_name) for i in range(len(files))]
                for future in as_completed(futures):
                    pbar.update(1)

    elif type == 'zip':
        files = []
        for file_path in file_paths:
            files.extend(glob(os.path.join(file_path, '*')))
        names = [f'{prefix}_{i}' for i in range(idx, idx+len(files))]

        with tqdm(files) as pbar:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(upload_zip, files[i], names[i],
                                           team_name, template_name, compress) for i in range(len(files))]
                for future in as_completed(futures):
                    pbar.update(1)

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


def upload_zip(file_path, name, team_name, template_name, compress=True):
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
