import requests

def request(url, method, token='', *args, **kwargs):
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
    rsp = getattr(requests, method)(url, headers=headers, *args, **kwargs)
    return rsp
