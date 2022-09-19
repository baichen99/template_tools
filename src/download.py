import os
import requests
from tqdm import tqdm
from xml.etree import ElementTree as ET

from template_tools.src.request import request
from template_tools.src.urls import download_url, base_url
from template_tools.src.info import get_all_data


def download_all_xmls(team_name, template_name, output_dir, filter_callback=None):
    """download all xmls of template
    Args:
        :param template_name: 模板名称
        :param team_name: 团队名称
    """
    records = get_all_data(team_name, template_name,
                           filter_callback=filter_callback)
    all_id = [record['dataId'] for record in records]
    download_all_xmls_by_id(all_id, output_dir)

def download_all_zips(team_name, template_name, output_dir, filter_callback=None):
    """download all xmls of template
    Args:
        :param template_name: 模板名称
        :param team_name: 团队名称
    """
    records = get_all_data(team_name, template_name,
                           filter_callback=filter_callback)
    all_id = [record['dataId'] for record in records]
    download_all_zips_by_id(all_id, output_dir)

def download_all_xmls_by_id(all_id, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for id_ in tqdm(all_id):
        with open(os.path.join(output_dir, f'{id_}.xml'), mode='wb+') as f:
            rsp = requests.post(download_url, json={'dataId': id_})
            f.write(rsp.content)

def download_all_zips_by_id(all_id, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for id_ in tqdm(all_id):
        folder_path = os.path.join(output_dir, str(id_))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, 'data.xml')
        with open(file_path, mode='wb+') as f:
            rsp = requests.post(download_url, json={'dataId': id_})
            f.write(rsp.content)
        tree = ET.parse(file_path).getroot()
        files = tree.findall('.//_file')
        for file in files:
            name_node = file.find('.//_name')
            url_node = file.find('.//_url')
            name = name_node.text
            url = url_node.text
            if name and url:    
                rsp = requests.get(base_url + url)
                asset_path = os.path.join(folder_path, name)
                with open(asset_path, 'wb') as f:
                    f.write(rsp.content)
                url_node.text = f'import:{name}'
        new_xml_str = ET.tostring(tree, encoding='utf-8', method='xml', xml_declaration=True)
        with open(file_path, mode='wb') as f:
            f.write(new_xml_str)