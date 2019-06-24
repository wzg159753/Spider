import json
from multiprocessing import Pool
# from multiprocessing.pool import Pool

import requests
from datetime import datetime


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'xueqiu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

session = requests.Session()
session.headers = headers
# print(dir(session))
f = open('image/xueqiu.txt', 'w', encoding='UTF-8')

def write_json(list_data):
    for i in list_data:

        data = {i['name']: i}
        f.write(json.dumps(data)+'\n')
        print(data)



def get_response(url, params):
    # print(1)
    resp = download(url, params=params)
    list_data = resp.json()['data']['list']
    # print(list_data)
    write_json(list_data)
    # return list_data



def download(url, params=None, headers=None):

    resp = session.get(url, params=params, headers=headers)
    # print(resp.status_code)
    return resp

def run(params):
    url = 'https://xueqiu.com/service/v5/stock/screener/quote/list'
    # download(url, params)
    resp = get_response(url, params)
    # write_json(resp, f)



if __name__ == '__main__':
    resp = download('https://xueqiu.com/')
    pool = Pool(16)
    # f = open('image/xueqiu.txt', 'w', encoding='UTF-8')
    for city in ['CN', 'HK', 'US']:
        for i in range(1, 200):
            params = {
                'page': i,
                'size': '30',
                'order': 'desc',
                'orderby': 'percent',
                'order_by': 'percent',
                'market': city,
                'type': 'cn',
                '_': int(datetime.now().timestamp() * 1000)
            }
            url = 'https://xueqiu.com/service/v5/stock/screener/quote/list'

            pool.apply_async(func=run, args=(params, ))

    pool.close()
    pool.join()
    f.close()