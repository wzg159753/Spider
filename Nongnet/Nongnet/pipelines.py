# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class NongnetPipeline(object):

    def __init__(self, host, port):
        client = pymongo.MongoClient(host=host, port=port)
        dbs = client['v2ex']
        self.db = dbs['test']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings['MONGO_HOST'], port=crawler.settings['MONGO_PORT'])

    def process_item(self, item, spider):
        self.db.insert(dict(item))
        return item
