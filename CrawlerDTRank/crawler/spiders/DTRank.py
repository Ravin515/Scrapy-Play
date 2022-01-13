from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from crawler.spiders import util
from crawler.items import DTRankItem
import logging
import re
import copy
import json

class DTRank(Spider):
    name = 'DTRank'
    logger = util.set_logger(name, LOG_FILE_DTRank)

    def start_requests(self):
        page_num = 87
        for i in range(0, page_num + 1):
            urls = 'http://data.10jqka.com.cn/market/jgzy/field/enddate/order/desc/page/' + str(i)
            yield Request(url = urls, callback = self.parse)

    def parse(self, response):
        paths = response.xpath('//tbody/tr').extract()
        item = DTRankItem()
        for path in paths:
            date = Selector(text = path).xpath('//td[@class = "tc cur"]/text()').extract()[0]
            item['date'] = date

            stock_symbol = Selector(text = path).xpath('//td[@class="tc"][position() = 1]/a[@target = "_blank"]/text()').extract()[0]
            item['stock_symbol'] = stock_symbol

            stock_name = Selector(text = path).xpath('//td[@class="tc"][position() = 2]/a[@target = "_blank"]/text()').extract()[0]
            # stock_name = stock_name.decode("UTF-8")
            item['stock_name'] = stock_name

            buy_inst_num = Selector(text = path).xpath('//tr/td[@class="c-rise "]/text()').extract()[0]
            item['buy_inst_num'] = buy_inst_num

            sell_inst_num = Selector(text = path).xpath('//tr/td[@class="c-fall "]/text()').extract()[0]
            item['sell_inst_num'] = sell_inst_num

            rank_reason = Selector(text = path).xpath('//tr/td[@class = "tl "]/text()') .extract()[0] 
            # rank_reason = rank_reason.decode("UTF-8")
            item['rank_reason'] = rank_reason

            yield item
