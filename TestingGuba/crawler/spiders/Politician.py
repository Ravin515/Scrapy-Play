from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from datetime import datetime, timedelta
from crawler.items import PoliticianItem
import logging
import re
import copy

class PoliticianSpider(Spider):
    name = 'CrawlerPolitician'
    logger = util.set_logger(name, LOG_FILE_POLITICIAN)

    def start_requests(self):
        Polist = open("C:/Code/Testing/scrt.csv")
        lines = set(Polist.readlines())
        for line in lines:
            line = line.rstrip('\n')
            start_url = "http://www.chinavitae.com/biography/"
            yield Request(url = start_url+line+"/career", callback = self.parse)
        
    def parse(self, response):
        hxs = Selector(response)
        item = PoliticianItem()
        name = hxs.xpath('//div[@class="bioName"]/text()').extract()[0].strip()
        item['name'] = name
        try: #  borndate
            birth = response.xpath('//div[@class="bioDetails"]//text()').extract()
            if birth:
                birth = ' '.join(birth).strip()
                borndate = re.findall('\d+', birth)[0]
                item['born'] = borndate
        except Exception as ex:
            print("With no born:" + response.url) 

        careers = hxs.xpath('//tr[@valign="top"]').extract()
        for career in careers:
            duration = re.search('<td width="90" class="cdCell">(.+)<\/td>', career)
            if duration:
                duration = re.sub("—", "-", duration.group(1))
                item['duration'] = duration
            occupation = re.search('<strong>(.+)<\/strong>', career)
            if occupation:
                item['occupation'] = occupation.group(1).strip()
            branches = Selector(text = career).xpath('//a[contains(@class,"link11")]/text()').extract()[0].strip()         
            if branches:
                item['branch'] = branches
            yield item

    