# -*- coding: utf-8 -*-
import scrapy
import re
import execjs
import json



class JobSpiderSpider(scrapy.Spider):
    name = 'job_spider'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://www.zhaopin.com/']

    def parse(self, response):
        city_list = response.xpath('//div[@class="footerFuncCity clearfix"]/ul//a/@href').extract()
        for city in city_list:
            yield scrapy.Request('https:'+city, callback=self.city_page)


    def city_page(self, response):
        code = re.search(r'"code":"(.*?)"', response.text).group(1)
        req_id = re.search(r'var zpPageRequestId = (.*?)</script>', response.text).group(1)
        id = self.splict(req_id)
        # print(code)
        # print(id+'*'*20)
        for num in range(0,10):
            city_url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId=707&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&x-zp-page-request-id={}'.format(num*60, id)
            yield scrapy.Request(city_url, callback=self.job_page)

    #
    def job_page(self, response):
        result = json.loads(response.text)
        for url in result['data']['results']:
            self.logger.info(url['positionURL'])
    #
    def splict(self, req_id):
        return execjs.eval(req_id)





