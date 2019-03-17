# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NongchanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    subprice = scrapy.Field()
    qiding = scrapy.Field()
    supply_total = scrapy.Field()
    ship_time = scrapy.Field()
    position = scrapy.Field()
    effective = scrapy.Field()
    time = scrapy.Field()
