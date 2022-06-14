import os
import json
import shutil

from .request import request
from .upload import get_all_data
from .urls import download_url

def download_all_xmls(all_id, token, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for id_ in all_id:
        with open(os.path.join(output_dir, f'{id_}.xml'), mode='wb+') as f:
            rsp = request(download_url, 'post', token, json={'dataId': id_})
            f.write(rsp.content)
    