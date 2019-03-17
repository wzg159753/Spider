# -*- coding: utf-8 -*-
import scrapy
from ..items import NongchanItem


class NongSpiderSpider(scrapy.Spider):
    name = 'nong_spider'
    allowed_domains = ['zgncpw.com']
    start_urls = ['http://www.zgncpw.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        print(response.url)
        ul = response.xpath('//ul[@class="pos-abs one-li-new left-m"]/li')
        for li in ul:
            items = NongchanItem()
            title = li.xpath('./a/span/text()')
            if title:
                items['title'] = title.extract_first()
    #             print(title.extract_first())
            suburl = li.xpath('./a/@href')
            if suburl:
                yield scrapy.Request(suburl.extract_first(), callback=self.detail_page, meta={'items': items})

    def detail_page(self, response):
        url_list = response.xpath('//a[@class="font-gray-5"]/@href')
        if url_list:
            for url in url_list:
                yield scrapy.Request(url.extract(), callback=self.data_page, meta={'items': response.meta['items']})
    #
    def data_page(self, response):
        data = response.xpath('//ul[@class="two l-big line-height-36 clearfix"]/li')
        name = ['subprice', 'qiding', 'supply_total', 'ship_time', 'position', 'effective', 'time']
        if data:
            for num, li in enumerate(data):
                items = response.meta.get('items')
                if data[num]:
                    if data[num] == 3:
                        items[name[num]] = ''.join(data[3].css('::text')[1:].extract()).replace(' ', '')
                    else:
                        items[name[num]] = data[num].css('li::text').extract_first()
                    yield items














        # if data[0]:
        #     subprice = data[0].css('li::text').extract_first()
        # if data[1]:
        #     qiding = data[1].css('li::text').extract_first()
        # if data[2]:
        #     supply_total = data[2].css('li::text').extract_first()
        # if data[3]:
        #     ship_time = ''.join(data[3].css('::text').extract()[1:]).replace(' ', '')
        # if data[4]:
        #     position = data[4].css('li::text').extract_first()
        # if data[5]:
        #     effective = data[5].css('li::text').extract_first()
        # if data[6]:
        #     time = data[6].css('li::text').extract_first()
