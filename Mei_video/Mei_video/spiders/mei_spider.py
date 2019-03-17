# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import MeiVideoItem
from scrapy_redis.spiders import RedisSpider


class MeiSpiderSpider(RedisSpider):
    name = 'mei_spider'
    # allowed_domains = ['meipai.com']
    start_urls = ['https://www.meipai.com/']
    base_url = 'https://www.meipai.com'
    redis_key = 'mei_spider:start_urls'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        div = response.xpath('//div[@class="nav max center pr"]/a')
        if div:
            for a in div:
                url = a.css('a.dbl::attr(href)').extract_first()
                name = a.css('a.dbl::text').extract_first().strip()
                if '/live' is not url:
                    yield scrapy.Request(self.base_url+url, callback=self.detail_page, meta={'name': name})

    def detail_page(self, response):
        data_id = response.css('h1::attr(data-id)').extract_first()
        for num in range(1,6):
            url= "https://www.meipai.com/topics/hot_timeline?page={}&tid={}".format(num, data_id)
            yield scrapy.Request(url, callback=self.json_page, meta={'name': response.meta['name']})

    def json_page(self, response):
        data = json.loads(response.text)
        for video in data['medias']:
            items = MeiVideoItem()
            items['video_code'] = video['video']
            items['title'] = video['caption_origin']
            items['name'] = response.meta['name']
            yield items

