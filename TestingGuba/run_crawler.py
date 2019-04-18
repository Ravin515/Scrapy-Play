import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
spider_name = 'soda_green'
#spider_name = 'CrawlerGubaUserInfo2'
#spider_name = 'CrawlerPolitician'
#spider_name = 'CrawlerHotelaah'
#spider_name = 'cit_info'

process.crawl(spider_name)
process.start()
