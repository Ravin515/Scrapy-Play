# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from re import UNICODE
from crawler.spiders import util
from crawler.settings import *
# from scrapy import signals
import json
import pymongo
# import logging
# from scrapy.exporters import CsvItemExporter
# from datetime import date

class GBFPipeline(object):
    collection_name= 'GubaFuture'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item

class MongoPipeline(object):
    def __init__(self):
        # set logger
        self.logger = util.set_logger('pipeline', LOG_FILE_PIPELINE)

        # 建立MongoDB server
        self.db = util.set_mongo_server()

        # 建立redis server
        self.redis_server = util.set_redis_server()

    
    def process_item(self, item, spider):
        try:
            # 如果item又有content又有fp，正常处理
            if "content" in item:
                #判断 item['content'] 是否是 dict 
                content = item['content']
                if type(content) == dict:
                    self.db[spider.name].insert(content)
                elif type(content) == UNICODE:
                    content = json.loads(content)
                    self.db[spider.name].insert(content)
                else:
                    self.logger.warn('Pipeline Error (unknown content type): %s %s' % (spider.name, str(type(content)), item['url']))

        except Exception as ex:
            self.logger.warn('Pipeline Error (others): %s %s' % (str(ex),  str(item['url'])))
