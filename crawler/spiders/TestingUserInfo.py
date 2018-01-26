from crawler.spiders import util
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy.utils.request import request_fingerprint
from crawler.items import GubaItem
from crawler.settings import *
import pymongo
import logging
import json
import re

class GubaUserInfo(Spider):
    name = 'CrawlerGubaUserInfo2'
    
    def start_request(self):
        conn = pymongo.MongoClient('localhost', 27017)
        db = conn.test
        print(db)
        