import requests

def request(url, method, token='', *args, **kwargs):
    headers = kwargs.get('headers', {}) or {
        'Proxy-Connection': 'keep-alive',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    }
    rsp = getattr(requests, method)(url, headers=headers, *args, **kwargs)
    return rsp
