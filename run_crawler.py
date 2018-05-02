import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
#spider_name = 'CrawlerGuba2'
#spider_name = 'CrawlerGubaUserInfo2'
spider_name = 'CrawlerPolitician'
#spider_name = 'CrawlerHotelaah'
process.crawl(spider_name)
process.start()
