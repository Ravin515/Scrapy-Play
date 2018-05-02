# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from crawler.spiders import util
from crawler.settings import *
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import json
import logging

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
                elif type(content) == unicode:
                    content = json.loads(content)
                    self.db[spider.name].insert(content)
                else:
                    self.logger.warn('Pipeline Error (unknown content type): %s %s' % (spider.name, str(type(content)), item['url']))

        except Exception as ex:
            self.logger.warn('Pipeline Error (others): %s %s' % (str(ex),  str(item['url'])))

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')
    def close_spider(self, spider):
        self.file.close()
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class CSVPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('scrt_info.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item