# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import PearVideoItem


class PearSpiderSpider(scrapy.Spider):
    name = 'Pear_spider'
    allowed_domains = ['pearvideo.com']
    start_urls = ['https://www.pearvideo.com/']
    base_url = 'https://www.pearvideo.com/'
    jsp_url = 'https://www.pearvideo.com/category_loading.jsp?reqType={}&categoryId={}'

    def parse(self, response):
        ul = response.xpath('//ul[@class="head-banner"]/li')[:-1]
        if ul:
            for li in ul:
                url = li.xpath('./a[@class="menu"]/@href').extract_first()
                if 'live' not in url or 'panorama' not in url:
                    yield scrapy.Request(self.base_url+url, callback=self.class_page)

    def class_page(self, response):
        reqType = re.search(r'reqType = "(.*?)"', response.text)
        if reqType:
            for num in range(10):
                yield scrapy.Request(self.jsp_url.format(reqType, num), callback=self.zri_page)
        else:
            base = 'https://www.pearvideo.com/panorama_loading.jsp?start={}'
            for num in range(10):
                yield scrapy.Request(base.format(num*10), callback=self.zri_page)

    def zri_page(self, response):
        uls = response.css('a.vervideo-lilink.actplay::attr(href)')
        if uls:
            for url in uls:
                yield scrapy.Request(self.base_url + url.extract(), callback=self.detail_page)

    def detail_page(self, response):
        items = PearVideoItem()
        title = response.css('#poster img::attr(alt)')
        if title:
            items['title'] = title.extract_first()
        url = re.search(r'srcUrl="(.*?)"', response.text)
        if url:
            items['url'] = url.group(1)
        yield items
