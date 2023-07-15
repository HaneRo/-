# -*- encoding: utf-8 -*-

import requests


class Reptile:
    def __init__(self, url):
        # 定义基本参数
        super().__init__()
        self.search_url = url+'/search'
        self.encoding = 'utf-8'
        self.directory_url = url+'/catalog'
        self.info_url = url+'/info'
        self.content_url = url+'/content'
        Cookie = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Danger hiptop 3.4; U; AvantGo 3.2)',
            'Cookie': Cookie
        }

    def search(self, keywords, page=1):
        # 获得书本基本信息
        params = {
            'query': keywords,
            'page': page
        }
        res = self.getHtml(
            self.search_url,
            params
        )
        list = []
        for info in res['data']['search_tabs'][0]['data']:
            if 'book_data' in info.keys():
                list.append([info['book_data'][0]['book_id'], info['book_data']
                            [0]['book_name'], info['book_data'][0]['author']])
        return list

    def direct(self, book_id):
        # 获取书本目录
        params = {
            'book_id': book_id
        }
        res = self.getHtml(
            self.directory_url,
            params
        )
        list = []
        if 'catalog_data' in res['data']['data']:
            for data in res['data']['data']['catalog_data']:
                list.append([data['item_id'], data['catalog_title']])
        elif 'item_data_list' in res['data']['data']:
            for data in res['data']['data']['item_data_list']:
                list.append([data['item_id'], data['title']])
        else:
            print("未知目录格式,book id="+book_id)
            exit()

        return list

    def content(self, item_id):
        # 获取当前章节正文内容
        params = {
            'item_id': item_id
        }
        content_info = self.getHtml(
            self.content_url,
            params
        )
        return [content_info['data']['data']['novel_data']['volume_name'], content_info['data']['data']['novel_data']['title'], content_info['data']['data']['content']]

    def getHtml(self, url, params):
        res = requests.get(url, params)
        return res.json()
