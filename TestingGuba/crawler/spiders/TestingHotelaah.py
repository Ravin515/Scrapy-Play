from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from datetime import datetime, timedelta
from crawler.items import HotelaahItem
import logging
import re
import copy

class HotelaahSpider(Spider):
    name = 'CrawlerHotelaah'
    logger = util.set_logger(name, LOG_FILE_POLITICIAN)
    
    def start_requests(self):
        start_url = 'http://www.hotelaah.com/liaoning/dijishi.html'
        yield Request(url = start_url, callback = self.parse)
    
    def parse(self, response):
        citylist = response.xpath('//td/a[not(contains(@href, "index")) and not(contains(@href, "dijishi")) and not(contains(@href, "ditu")) and not(contains(@href, "www"))]').extract()
        
        for city in citylist:         
            item = HotelaahItem()
            city_name = Selector(text = city).xpath('//a/text()').extract()[0]
            item['city_name'] = city_name
            print(item)
            city_url = Selector(text = city).xpath('//a/@href').extract()[0]
            print(city_url)
            yield Request(url = 'http://www.hotelaah.com/liren/'+ 'liaoning' + '_' + city_url, meta = {'item': copy.deepcopy(item)}, callback = self.parse_mayor)

    def parse_mayor(self, response):
        pass
#    def parse(self, response):
#        filter_body = response.body.decode("utf8")
#        filter_body = re.sub('<[A-Z]+[0-9]*[^>]*>|</[A-Z]+[^>]*>', '', filter_body)

#        tables1 = Selector(text = filter_body).xpath('//*[contains(text(), "任期")]/parent::*/parent::*').extract()[0]
#        tables1 = Selector(text = tables1).xpath('//tr[position()>1]').extract()
#        for table1 in tables1:
#            duration = Selector(text = table1).xpath('//td[1]/text()').extract()[0].strip()
#            if duration:
#                item = duration
#            else:
#                item = "NA"
#            print(item)
      
#            try:
#                name = Selector(text = table1).xpath('//td[2]/text()').extract()[0].strip()
#            except:
#                try:
#                    name = Selector(text = table1).xpath('//td[2]/span/text()').extract()[0].strip()
#                except Exception as ex:
#                    print("With no name: " + response.url)


#        tables2 = Selector(text = filter_body).xpath('//*[contains(text(), "任期")]/parent::*/parent::*').extract()[1]
#        tables2 = Selector(text = tables2).xpath('//tr[position()>1]').extract()

#        for table2 in tables2:
#            duration = Selector(text = table2).xpath('//td[1]/text()').extract()[0].strip()
#            if duration:
#                item = duration
#            try:
#                name = Selector(text = table2).xpath('//td[2]/text()').extract()[0].strip()
#            except:
#                try:
#                    name = Selector(text = table2).xpath('//td[2]/span/text()').extract()[0].strip()
#                except Exception as ex:
#                    print("With no name: " + response.url)

