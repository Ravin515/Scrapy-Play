from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from datetime import datetime, timedelta
from crawler.items import CitItem
import logging
import re

class sodaspider(Spider):
    name = "soda_green"
    logger = util.set_logger(name, LOG_FILE_SODA)

    def start_requests(self):
        start_url = "https://music.163.com/#/artist/album?id=12707&limit=48"
        yield Request(url = start_url, callback = self.parse)

    def parse(self, response):
        print(response)
        pass
            