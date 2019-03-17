# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import re

class PearVideoPipeline(object):
    def process_item(self, item, spider):
        content = requests.get(item['url']).content
        name = re.sub(r'[? * ！ $ #]]','',item['title'])
        with open('E:/untitled1/video/{}.mp4'.format(name), 'wb') as f:
            f.write(content)
        return item
