# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NongnetItem
from scrapy_redis.spiders import RedisCrawlSpider
import re


class NongSpiderSpider(RedisCrawlSpider):
    name = 'nong_spider'
    # allowed_domains = ['nongnet.com']
    # start_urls = ['http://www.nongnet.com/']
    '''<a  href="(.*?)" class=".*?"'''
    redis_key = 'nong_spider:start_urls'
    base_url = 'http://www.nongnet.com'

    rules = (
        Rule(LinkExtractor(allow=r'\/default.aspx\?PageID=\d+&classid=0&itype=2&prv=&city=&county='), callback='parse_item_page', follow=True),
        # Rule(LinkExtractor(allow=r'\/xinxi\/\d+\w\d+\.aspx'), callback='parse_item', follow=False),

    )


    def parse_item_page(self, response):

        div = response.xpath('//div[@id="ContentMain_lblList"]/ul')
        if div:
            for ul in div:
                items = NongnetItem()
                guanxi = ul.css('font::text')
                if guanxi:
                    items['guanxi'] = guanxi.extract_first()
                title = ul.css('li.lileft a::text')
                if title:
                    items['title'] = title.extract_first()
                position = ul.css('li.lileft2 a::text')
                if position:
                    items['position'] = '|'.join(position.extract())
                url = ul.css('li.lileft a::attr(href)')
                if url:
                    yield scrapy.Request(self.base_url+url.extract_first(), callback=self.parse_item, meta={'items': items})


    def parse_item(self, response):
        items = response.meta['items']
        phone = re.search(r"手机号码</div><div class='xinxisxr'>(.*?)</div>", response.text)
        if phone:
            items['phone'] = phone.group(1)
        name = re.search(r"联 系 人</div><div class='xinxisxr'>(.*?)</div>", response.text)
        if name:
            items['name'] = name.group(1)
        shangshi = re.search(r"上市时间</div><div class='xinxisxr'>(.*?)</div>", response.text)
        if shangshi:
            items['shangshi'] = shangshi.group(1)
        time = re.search(r"color='999999'>时间：(.*?) &nbsp;", response.text)
        if time:
            items['time'] = time.group(1)

        yield items