# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os
import requests
import execjs
from .settings import MP4_PATH



class MeiVideoPipeline(object):

    def open_spider(self, spider):
        self.f = open(r'E:\untitled1\Mei_video\Mei_video\spiders\aa.js', 'r')
        self.result = execjs.compile(self.f.read())

    def process_item(self, item, spider):
        url = self.result.call("decode", item['video_code'])
        src_mp4 = requests.get(url).content
        name = re.sub('[\\n : ? / ！]', '', item['title'])
        dirct = item['name']
        if not os.path.exists(MP4_PATH+dirct):
            os.mkdir(MP4_PATH+dirct)
        with open(MP4_PATH+'{}/{}.mp4'.format(dirct, name), 'wb') as f:
            f.write(src_mp4)
        return item

    def close_spider(self, spider):
        self.f.close()