import os

from .request import request
from .urls import download_url
from .upload import get_all_data

def download_all_xmls(template_name, team_name, token, output_dir):
    """download all xmls of template
    Args:
        :param template_name: 模板名称
        :param team_name: 团队名称
    """
    records = get_all_data(team_name, template_name, token, num=1000000).get('records', [])
    all_id = [record['dataId'] for record in records]
    download_all_xmls_by_id(all_id, token, output_dir)

def download_all_xmls_by_id(all_id, token, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for id_ in all_id:
        with open(os.path.join(output_dir, f'{id_}.xml'), mode='wb+') as f:
            rsp = request(download_url, 'post', token, json={'dataId': id_})
            f.write(rsp.content)
    