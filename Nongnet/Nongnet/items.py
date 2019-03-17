# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NongnetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    guanxi = scrapy.Field()
    title = scrapy.Field()
    position = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()
    shangshi = scrapy.Field()
    time = scrapy.Field()



