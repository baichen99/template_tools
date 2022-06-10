import os
import json
import requests

def request(url, method, token='', *args, **kwargs):
    headers = kwargs.get('headers', {})
    if not headers:
        headers = {
            'Authorization': f'Bearer {token}',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
            'Content-Type': 'application/json;charset=UTF-8'
        }
    rsp = getattr(requests, method)(url, headers=headers, *args, **kwargs)
    return rsp
