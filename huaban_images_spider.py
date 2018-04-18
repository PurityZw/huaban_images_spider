# -*- coding:utf-8 -*-
import re
import requests
from lxml import etree
from utlis.utlis import SpiderVariable


class DoubanImagesSpider(object):
    def __init__(self):
        # http://huaban.com/boards/favorite/beauty/
        self.root_url = 'http://huaban.com/'
        self.image_domin = 'http://img.hb.aicdn.com/'
        self.image_path = './images/'
        self.image_suffix = {
            'image/jpeg': '.jpg',
            'image/png': '.png'
        }

    def send_request(self, url, proxyAddr=None, headers=None, params=None):
        """
        发送请求
        :param url: 请求地址
        :return: 响应对象
        """
        # print url
        # print params
        try:
            response = requests.get(url, proxies=proxyAddr, headers=headers, params=params)
            return response
        except Exception as e:
            print e
            return None

    def parse_page_list(self, response):
        """
        分析页面中URL列表
        :param response: html的响应对象
        :return: 匹配列表
        """
        html = response.content
        html_obj = etree.HTML(html)
        url_list = html_obj.xpath("//div")
        # print len(url_list)
        return url_list

    def write_file(self, fileName, fileData):
        """
        写入文件
        :param fileName: 写入文件名称
        :param fileData: 写入文件内容
        :return:
        """
        with open(self.image_path + fileName, 'wb') as f:
            f.write(fileData)

    def main(self):
        """
        主函数
        :return:
        """
        proxy_addr = {'http': 'http://' + SpiderVariable().get_random_proxy_addr()}
        headers = {
            "Accept": "application/json",
            "Connection": "keep-alive",
            "Host": "huaban.com",
            "X-Request": "JSON",
            "X-Requested-With": "XMLHttpRequest"
        }
        headers['User-Agent'] = SpiderVariable().get_random_user_agent()
        # url = self.root_url + 'pin/1590844261/'
        url = 'http://huaban.com/boards/favorite/beauty/'

        params = {
            "jg25rkfp": '',
            "max": '1590848207',
            "limit": '20',
            "wfl": '1',
        }

        # 请求数据
        response = self.send_request(url, proxy_addr, headers, params=params)
        boards_list = response.json()['boards']

        i = 0
        # 解析json数据
        for board in boards_list:
            for pin in board['pins']:
                domin_url = self.image_domin + pin['file']['key']
                img_data = self.send_request(domin_url)
                file_name = str(pin['pin_id']) + self.image_suffix[pin['file']['type']]
                print '下载第' + str(i + 1) + '张图片,' + file_name
                self.write_file(file_name, img_data.content)
                i += 1


if __name__ == '__main__':
    spider = DoubanImagesSpider()
    spider.main()
