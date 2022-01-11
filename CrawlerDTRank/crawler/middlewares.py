# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
# from selenium import webdriver
from scrapy.http import HtmlResponse
# import selenium.webdriver.support.ui as ui

class RandomRequestHeaders(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents, cookies):
        self.agents = agents
        self.cookies = cookies

    @classmethod
    def from_crawler(cls, crawler):
        ua = crawler.settings.getlist('USER_AGENT')
        ck = crawler.settings.getlist('COOKIES')
        return cls(ua, ck)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))       

# class IdMiddleware(object):
#     # 通过chrome请求动态网页，代替scrapy的downloader

#     def process_request(self, request, spider):
#         if spider.name == "artist_id":
#             print ("Chrome is starting...")
#             driver = webdriver.Chrome('C:/Code/Scrapy-Play/CrawlerNetMusic/chromedriver.exe') #指定使用的浏览器
#             driver.get(request.url)
#             driver.switch_to.frame('g_iframe') #移动到 iframe
#             wait = ui.WebDriverWait(driver, 15)
#             body = driver.page_source
#             return HtmlResponse(url = request.url, body=body, encoding='utf-8', request = request)