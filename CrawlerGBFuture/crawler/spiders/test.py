from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from crawler.spiders import util
from crawler.items import MntItem
import re
from datetime import date
from datetime import datetime

class GBFuture(Spider):
    name = 'GBFuturetest'
    logger = util.set_logger(name, LOG_FILE_GBFuture)

    def start_requests(self):
        start_url = "http://guba.eastmoney.com/list,rb,f_1.html"
        item = MntItem()
        item['content'] = {}
        item['content']['bar_name'] = "螺纹钢吧"
        yield Request(url = start_url, callback = self.parse, dont_filter = True, meta = {'page': 1, 'item': item})

    def parse(self, response): # 确定需要抓取的页数
        page = response.meta['page']
        item = response.meta['item']
        dates = response.xpath('//div[contains(@class, "normal_post")]//span[contains(@class, "l5")]/text()').extract()
        md = date.today().strftime("%m-%d")

        tag_date = [] # 提取时间的前4个字符
        for d in dates:
            tag_date.append(d[:5])
        tag_date = set(tag_date)

        if md in tag_date:
            yield Request(url = 'http://guba.eastmoney.com/list,rb,f_' + str(page + 1) + '.html', callback = self.parse, dont_filter = True, meta = {'page': page + 1, 'item' : item})
        
        elif md not in tag_date:
            for i in range(1, page):
                yield Request(url = 'http://guba.eastmoney.com/list,rb,f_' + str(i) + '.html', callback = self.parse_page, dont_filter = True, meta = {'item' : item, 'md': md})
        
    def parse_page(self, response):
        item = response.meta['item']
        md = response.meta['md']
        hxs = response.xpath('//div[contains(@class, "normal_post")]').extract()
        for hx in hxs:
            post_date = Selector(text = hx).xpath('//span[contains(@class, "l5")]/text()').extract()[0]
            post_tag_date = post_date[:5]
            if post_tag_date == md:
                try:
                    post_date = Selector(text = hx).xpath('//span[contains(@class, "l5")]/text()').extract()[0]
                    post_date = str(date.today().year) + "-" + post_date            
                    post_date = datetime.strptime(post_date, "%Y-%m-%d %H:%M")
                    item['content']['post_date'] = post_date
                except:
                    pass
                try:
                    post_title = Selector(text = hx).xpath('//span[contains(@class, "l3")]/a/@title').extract()[0]
                    item['content']['post_title'] = post_title
                except:
                    pass
                try:
                    reply_num = Selector(text = hx).xpath('//span[contains(@class, "l2")]/text()').extract()[0]
                    item['content']['reply_num'] = reply_num
                except:
                    pass
                try:
                    read_num = Selector(text = hx).xpath('//span[contains(@class, "l1")]/text()').extract()[0]
                    item['content']['read_num'] = read_num
                except:
                    pass
                try:
                    post_author = Selector(text = hx).xpath('//span[contains(@class, "l4")]/a[@target = "_blank"]/font/text()').extract()[0]
                    item['content']['post_author'] = post_author
                except:
                    pass
                try:
                    author_title = Selector(text = hx).xpath('//span[contains(@class, "l4")]/a/em/@title').extract()[0]
                    item['content']['author_title'] = author_title
                except:
                    pass
                yield item
