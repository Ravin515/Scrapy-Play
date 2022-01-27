import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
#spider_name = 'GBFuture'
spider_name = 'GBFuturetest'
process.crawl(spider_name)
process.start()