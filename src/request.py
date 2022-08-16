import json
import requests
from template_tools.settings import token
from retrying import retry


@retry(stop_max_attempt_number=3)
def request(url, method, token=token, *args, **kwargs):
    headers = kwargs.get('headers', {}) or {
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    }
    if kwargs.get('headers'):
        kwargs.pop('headers')
    try:
        rsp = getattr(requests, method)(url, headers=headers, *args, **kwargs)
    except Exception as e:
        print(e)
    return json.loads(rsp.text)
