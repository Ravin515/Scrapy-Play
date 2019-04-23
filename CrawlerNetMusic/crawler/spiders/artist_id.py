from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from datetime import datetime, timedelta
from crawler.items import NetItem
import logging
import re
import copy
import json
from selenium import webdriver

class ArtistSpider(Spider):
    name = 'artist_id'
    #allow_domains = ['music.163.com']
    logger = util.set_logger(name, LOG_FILE_ARTIST)

    def start_requests(self):
        ls1 = [1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003]    # id
        ls2 = [0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]   # initial
        for i in ls1:
            for j in ls2:
                start_url = 'https://music.163.com/#/discover/artist/cat?id='+ str(i) + '&initial=' + str(j)
                yield Request(url = start_url, callback = self.parse)
        #start_url = 'https://music.163.com/#/discover/artist/cat?id=1001&initial=0'
        #yield Request(url = start_url, callback = self.parse)

    def parse(self, response):
        item = NetItem()
        hxs = response.body.decode("utf-8")
        paths = Selector(text = hxs).xpath('//li//a[@class="nm nm-icn f-thide s-fc0"]').extract()
        for path in paths:
            ids = Selector(text = path).xpath('//a/@href').extract()[0]
            id = re.search("\?id=(.+)", ids).group(1)
            item['artist_id'] = id
            name = Selector(text = path).xpath('//a/text()').extract()[0]
            item['artist_name'] = name
            yield item

        #names1 = response.xpath('//li[@class="sml"]/a[@class="nm nm-icn f-thide s-fc0"]').extract()
        #for name in names1:
        #    ids = Selector(text = name).xpath('//a/@href').extract()[0]
        #    id = re.search("\?id=(.+)", ids).group(1)
        #    item['content']['artist_id'] = id
            
                