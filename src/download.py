import os
import requests
from tqdm import tqdm

from template_tools.src.request import request
from template_tools.src.urls import download_url
from template_tools.src.info import get_all_data


def download_all_xmls(template_name, team_name, output_dir, filter_callback=None):
    """download all xmls of template
    Args:
        :param template_name: 模板名称
        :param team_name: 团队名称
    """
    records = get_all_data(team_name, template_name,
                           filter_callback=filter_callback)
    all_id = [record['dataId'] for record in records]
    download_all_xmls_by_id(all_id, output_dir)


def download_all_xmls_by_id(all_id, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for id_ in tqdm(all_id):
        with open(os.path.join(output_dir, f'{id_}.xml'), mode='wb+') as f:
            # rsp = request(download_url, 'post', json={'dataId': id_})
            rsp = requests.post(download_url, json={'dataId': id_})
            f.write(rsp.content)
