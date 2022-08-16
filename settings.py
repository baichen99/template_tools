import requests
import json

# 下面是自定义设置
username = ''
password = ''

# base_url = 'http://matdata.shu.edu.cn'
base_url = 'https://matdata.cloud'


# 下面内容不要修改
def get_token(username, password):
    login_url = base_url + '/mgd/api/user/login'

    data = {
        'account': username,
        'password': password
    }
    try:
        rsp = requests.post(login_url, json=data)
        token = json.loads(rsp.text)['data']['token']
        return token
    except Exception as e:
        raise Exception(f"Cannot get token: {str(e)}")


token = get_token(username, password)
