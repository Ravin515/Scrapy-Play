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

class ArtistSpider(Spider):
    name = 'artist_id'
    logger = util.set_logger(name, LOG_FILE_ARTIST)


    def start_requests(self):
        allowed_domains = ['music.163.com']
        group_ids = (1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003)
        initials = [i for i in range(65,90)] + [0]
        for gid in group_ids:
            for initial in initials:
                url = 'https://music.163.com/api/artist/list?cat={gid}&initial={initial}&limit=100'.\
                    format(gid = gid, initial = initial)
                yield Request(url = copy.deepcopy(url), callback = self.parse)

    def parse(self, response):
        hxs = response.body.decode('utf-8')
        hxs = json.loads(hxs)
        item = NetItem()
        item['content'] = {}
        print(hxs)
        artists = copy.deepcopy(hxs['artists'])
        for artist in artists:
            if artist['name']:
                item['content']['name'] = artist['name']
            if artist['id']:
                item['content']['id'] = artist['id']
            try:
                artist['accountId']
                item['content']['account_id'] = artist['accountId']
            except:
                item['content']['account_id'] = "NULL"
            if artist['alias']:
                item['content']['alias'] = artist['alias']
            yield item
