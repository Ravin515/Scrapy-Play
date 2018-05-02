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
    #name = 'CrawlerHotelaah'
    #logger = util.set_logger(name, LOG_FILE_POLITICIAN)
    def start_requests(self):
        start_url = "http://www.hotelaah.com"
        yield Request(url = start_url, callback = self.parse)
    
    def parse(self, response):
        provin_names = response.xpath('//td[@width="42"]/a[contains(@href, "index.html")]').extract()
        for name in provin_names:
            item = HotelaahItem()
            province_name = Selector(text = name).xpath('//text()').extract()[0]
            item['province_name'] = province_name
            province_url = Selector(text = name).xpath('//a/@href').extract()[0]
            province_pinyin = re.search('(.+)/index.html', province_url).group(1)
            province_url = 'http://www.hotelaah.com/' + province_url
            yield Request(url = province_url, meta = {'item': item, 'pinyin' : province_pinyin}, callback = self.parse_city)
    
    def parse_city(self, response):
        url = response.xpath('//a[@href="dijishi.html"]').extract()
        pinyin = response.meta['pinyin']
        item = response.meta['item']
        if url:
            yield Request(url = 'http://www.hotelaah.com/' + pinyin + '/dijishi.html', meta = {'item': copy.deepcopy(item), 'pinyin': copy.deepcopy(pinyin)}, callback = self.parse_citylist)
        else:
            yield Request(url = 'http://www.hotelaah.com/liren/' + pinyin + '.html', meta = {'item': copy.deepcopy(item)},callback = self.parse_mayor)

    def parse_citylist(self, response):
        citylist = response.xpath('//td/a[not(contains(@href, "index")) and not(contains(@href, "dijishi")) and not(contains(@href, "ditu")) and not(contains(@href, "www"))]').extract()

        for city in citylist:
            item = response.meta['item']
            pinyin = response.meta['pinyin']            
            city_name = Selector(text = city).xpath('//a/text()').extract()[0]
            item['city_name'] = city_name
            city_url = Selector(text = city).xpath('//a/@href').extract()[0]
            yield Request(url = 'http://www.hotelaah.com/liren/'+ pinyin + '_' + city_url, meta = {'item': copy.deepcopy(item)}, callback = self.parse_mayor)

    def parse_mayor(self, response):
        item  = response.meta['item']
        if response.status == 200:
            try:
                filter_body = response.body.decode("utf8")
            except:
                try:
                    filter_body = response.body.decode("ANSI")
                except Exception as ex:
                    print("Decode webpage failed: " + response.url)
                    return

        filter_body = re.sub('<[A-Z]+[0-9]*[^>]*>|</[A-Z]+[^>]*>', '', filter_body)

        tables1 = Selector(text = filter_body).xpath('//*[contains(text(), "任期")]/parent::*/parent::*').extract()[0]
        tables1 = Selector(text = tables1).xpath('//tr[position()>1]').extract()
        for table1 in tables1:
            try:
                name = Selector(text = table1).xpath('//td[2]/text()').extract()[0].strip()
            except:
                try:
                    name = Selector(text = table1).xpath('//td[2]/span/text()').extract()[0].strip()
                except Exception as ex:
                    print("With no name: " + response.url)
            item['leader_name'] = name
            item['tag'] = "scrt"

            try:
                duration = Selector(text = table1).xpath('//td[1]/text()').extract()[0]
                item['duration'] = copy.deepcopy(duration)
            except Exception as ex:
                item['duration'] = 'no'
                print("With no duration: " + response.url)
            yield item


        tables2 = Selector(text = filter_body).xpath('//*[contains(text(), "任期")]/parent::*/parent::*').extract()[1]
        tables2 = Selector(text = tables2).xpath('//tr[position()>1]').extract()

        for table2 in tables2:
            try:
                name = Selector(text = table2).xpath('//td[2]/text()').extract()[0].strip()
            except:
                try:
                    name = Selector(text = table2).xpath('//td[2]/span/text()').extract()[0].strip()
                except Exception as ex:
                    print("With no name: " + response.url)
            item['leader_name'] = name
            item['tag'] = "mayor"

            try:
                duration = Selector(text = table2).xpath('//td[1]/text()').extract()[0]
                item['duration'] = copy.deepcopy(duration) 
            except Exception as ex:
                item['duration'] = 'no'
                print("With no duration: " + response.url)
            yield item

            


