from tqdm import tqdm

from .request import request
from .urls import delete_url
from .upload import get_all_data


def delete_all(team_name, template_name, token):
    """delete all data of template"""
    records = get_all_data(team_name, template_name, token, num=1000000).get('records', [])
    all_id = [record['dataId'] for record in records]
    for id_ in tqdm(all_id):
        data = {
            'dataId': id_
        }
        rsp = request(delete_url, 'post', token=token, json=data)
        if rsp.status_code != 200:
            print(rsp.text)


def delete(all_id, token):
    """delete all data of template"""
    for id_ in all_id:
        data = {
            'dataId': id_
        }
        rsp = request(delete_url, 'post', token, json=data)
        if rsp.status_code != 200:
            print(rsp.text)

if __name__ == '__main__':
    pass