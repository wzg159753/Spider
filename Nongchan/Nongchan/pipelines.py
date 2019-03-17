# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .settings import MONGO_HOST, MONGO_PORT

class NongchanPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        database = client['v2ex']
        self.db = database['nongchan']

    def process_item(self, item, spider):
        self.db.insert(dict(item))
        return item
