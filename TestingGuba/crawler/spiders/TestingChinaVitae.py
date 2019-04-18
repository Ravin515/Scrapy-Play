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
    #name = 'CrawlerPolitician'
    #logger = util.set_logger(name, LOG_FILE_POLITICIAN)


    def start_requests(self):
        start_url = "http://www.chinavitae.com/biography/Xi_Jinping/full"
        item = PoliticianItem() 
        item['branch'] = []
        yield Request(url = start_url, meta = {'item': item}, callback = self.parse)

    def parse(self, response):
        hxs = Selector(response)       
        item = response.meta['item']

        try: # whole of biography
            bigph = hxs.xpath('//div[@id="dataPanel"]/p').extract()[0].strip()
            bigph = re.sub('\r\n', ' ', bigph)
            bigph = re.sub('<br>', '', bigph)
            bigph = re.search('<p>(.+)<\/p>', bigph).group(1)
            item['branch'] = bigph
            print(item)
        except Exception as ex:
            print("With no bigph:" + response.url)
                
        birth = hxs.xpath('//div[@class="bioDetails"]//text()').extract()
        if birth:
            birth = ' '.join(birth).strip()
            borndate = re.findall('\d+', birth)[0]
            birthplace = re.search('Birthplace:(.+)', birth).group(1)
            birthplace = re.sub(' ', '', birthplace)
            print(birthplace)
        careers = hxs.xpath('//tr[@valign="top"]').extract()
        career = {}
        for c in careers:
            duration = re.search('<td width="90" class="cdCell">(.+)<\/td>', c)
            if duration:
                duration = re.sub("—", "-", duration.group(1))
                career['duration'] = duration
            occupation = re.search('<strong>(.+)<\/strong>', c)
            if occupation:
                career['occupation'] = occupation.group(1)
            branch = Selector(text = c).xpath('//a[contains(@class,"link11")]/text()').extract()          
            if branch:
                career['branch'] = branch
                print(career)
            item['branch'].append(copy.deepcopy(career))

