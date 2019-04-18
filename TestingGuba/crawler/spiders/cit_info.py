from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from datetime import datetime, timedelta
from crawler.items import CitItem
import logging
import re
import copy

class citspider(Spider):
    name = "cit_info"
    logger = util.set_logger(name, LOG_FILE_CIT)

    def start_requests(self):
        start_url = "http://www.ccdi.gov.cn/special/zyxszt/"
        yield Request(url = start_url, callback = self.parse)

    def parse(self, response):
        inspt_urls = response.xpath('//div[@class="tith2"]//a/@href').extract()
        for inspt_url in inspt_urls:
            inspt_url = "http://www.ccdi.gov.cn/special/zyxszt" + re.sub("\.", "", inspt_url)
            yield Request(url = inspt_url, callback = self.parse_list, meta = {'inspt_url' : inspt_url})

    def parse_list(self, response):
        post_nums = response.xpath('//div[@class="page"]/script[@type = "text/javascript"]/text()').extract()[0]
        post_nums = re.search("\((\d?),.+\)", post_nums).group(1)
        inspt_url = response.meta['inspt_url']
        for post_num in post_nums:
            for i in range(1, int(post_num)+1):
                if i == 1:
                    page_url = inspt_url + "index.html"
                    yield Request(url = copy.deepcopy(page_url), callback = self.parse_page, meta = {'inspt_url': copy.deepcopy(inspt_url)})
                else:
                    page_url = inspt_url + "index_"+ str(i-1) + ".html"
                    yield Request(url = copy.deepcopy(page_url), callback = self.parse_page, meta = {'inspt_url': copy.deepcopy(inspt_url)})
                #print(page_url)

    def parse_page(self, response):
        #pass
        post_urls = response.xpath('//li[@class="fixed"]//a/@href').extract()
        for post_url in post_urls:
            inspt_url = response.meta['inspt_url']
            post_url = inspt_url + re.search("\.\/(.+)", post_url).group(1)
            yield Request(url = post_url, callback = self.parse_post)

    def parse_post(self, response):
        item = CitItem()
        inspt = response.xpath('//div[@class="fl"]/span').extract()[0]
        inspt = re.search("专题&gt;(.+)<\/span>", inspt).group(1)
        inspt_title = re.search("(.+)&gt;(.+)", inspt).group(1)
        item['inspt_title'] = inspt_title
        inspt_tag = re.search("(.+)&gt;(.+)", inspt).group(2)
        item['inspt_tag'] = inspt_tag

        title = response.xpath('//h2[@class="tit"]/text()').extract()[0].strip()
        item['title'] = title
        
        time = response.xpath('//em[@class="e2"]/text()').extract()[0].strip()
        time = re.search("发布时间：(.+)", time).group(1).strip()
        item['time'] = time
        
        content = response.xpath('//p[@align="justify"]/text()').extract()
        item['content'] = content
        yield item