from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from crawler.items import PoliticianItem
import logging
import re
import copy

class PoliticianSpider(Spider):
    #name = 'CrawlerPolitician'
    #logger = util.set_logger(name, LOG_FILE_POLITICIAN)
    
    #def start_requests(self):
    #    start_url = 'http://www.chinavitae.com/vip/index.php?mode=events&type=cv&id=270'
    #    yield Request(url = start_url, meta ={'url' : start_url}, callback = self.parse)
    
    #def parse(self, response):
    #    year = response.xpath('//p/a/text()').extract()
    #    year = ' '.join(year).strip()
    #    years = re.findall('\d{4}', year)
        
    #    for y in years:
    #        res_url = response.meta['url']
    #        yield Request(url = res_url+ '&filter_year='+y, callback = self.parse_list)

    #def parse_list(self, response):
    #    urls = response.xpath('//div[@class="link12b"]/a/@href').extract()
    #    for url in urls:
    #        vippurl = 'http://www.chinavitae.com'+url
    #        yield Request(url = vippurl, callback = self.parse_vipp)

    def start_requests(self):
        
        yield Request(url = 'http://www.chinavitae.com/vip/index.php?mode=show&id=1950', callback = self.parse_vipp)
    
    def parse_vipp(self, response):

        #acti = response.xpath('//html//tr[2]/td[2]').extract()[0]
        #acti = re.sub('\r\n', '', acti)
        #acti = re.search('td>(.+)<\/td', acti).group(1)
        
        infos = response.xpath('//*[contains(@class, "link12")]//text()').extract()
        infos = ','.join(infos).strip()
        infos = re.sub('\n', '', infos)
        infos = re.sub('\t', '', infos)
        print(infos)
        #print(infos)
        #date = re.search('Date: ,(.+),Activity', infos).group(1).strip()
        #location = re.search('Location: ,(.+),Attendees', infos).group(1).strip()
        #attendees = re.search('Attendees: ,(.+),Source', infos).group(1).strip()
        #source = re.search('Source: ,(.+),Topics', infos).group(1).strip()
        #topics = re.search('Topics: ,(.+)', infos).group(1).strip()
               