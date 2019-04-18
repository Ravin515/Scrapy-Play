from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from datetime import datetime, timedelta
from crawler.items import GubaItem
import logging
import re

class sodaspider(Spider):
    def start_requests(self):
        name = "soda_green"