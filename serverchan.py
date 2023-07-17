import requests


def send(key, title='', desp='', short='', channel='', openid=''):
    url = f'https://sctapi.ftqq.com/{key}.send'
    params = {
        'title': title,
        'desp': desp,
        'short': short,
        'channel': channel,
        'openid': openid
    }
    print(params)
    res = requests.get(url, params)
    if res.json()["code"] != 1:
        raise
    return res.json()
