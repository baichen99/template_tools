from tqdm import tqdm

from template_tools.src.request import request
from template_tools.src.urls import delete_url, batch_delete_url
from template_tools.src.info import get_all_data


def delete_all(team_name, template_name, filter_callback=None):
    """delete all data of template"""
    records = get_all_data(team_name, template_name,
                           filter_callback=filter_callback)
    all_id = [record['dataId'] for record in records]
    # use batch delete
    rsp = request(batch_delete_url, 'post', json={'dataIds': all_id})
    if rsp.get('msg') != 'success':
        print(rsp)


def delete_xml_by_id(all_id):
    """delete all data of template"""
    for id_ in tqdm(all_id):
        data = {
            'dataId': id_
        }
        rsp = request(delete_url, 'post', json=data)
        if rsp.get('msg') != 'success':
            print(rsp)


if __name__ == '__main__':
    pass
