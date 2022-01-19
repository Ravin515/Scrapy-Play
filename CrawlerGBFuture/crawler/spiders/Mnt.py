from multiprocessing import AuthenticationError
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from crawler.settings import *
from crawler.spiders import util
from crawler.items import MntItem
import re
from datetime import date

class GBFuture(Spider):
    name = 'GBFuture'
    logger = util.set_logger(name, LOG_FILE_GBFuture)

    def start_requests(self):
        start_url = "http://guba.eastmoney.com/list,rb,f_4.html"
        item = MntItem()
        item['content'] = {}
        item['content']['bar_name'] = "螺纹钢吧"
        yield Request(url = start_url, callback = self.parse, dont_filter = True, meta = {'page': 4, 'item': item})

    def parse(self, response):
        page = response.meta['page']
        item = response.meta['item']
        dates = response.xpath('//div[contains(@class, "normal_post")]//span[contains(@class, "l5")]/text()').extract()
        md = date.today().strftime("%m-%d")

        tag_date = [] # 提取时间的前4个字符
        for d in dates:
            tag_date.append(d[:5])
        tag_date = set(tag_date)

        hxs = response.xpath('//div[contains(@class, "normal_post")]').extract()
        if md in tag_date: # 如果该页都是当天的数据抓取之后全部翻页
            for hx in hxs:
                post_date = Selector(text = hx).xpath('//span[contains(@class, "l5")]/text()').extract()[0]
                post_tag_date = post_date[:5]
                if post_tag_date == tag_date:
                    post_date = Selector(text = hx).xpath('//span[contains(@class, "l5")]/text()').extract()[0]
                    item['content']['post_date'] = post_date
                    post_title = Selector(text = hx).xpath('//span[contains(@class, "l3")]/a/@title').extract()[0]
                    item['content']['post_title'] = post_title
                    reply_num = Selector(text = hx).xpath('//span[contains(@class, "l2")]/text()').extract()[0]
                    item['content']['reply_num'] = reply_num
                    read_num = Selector(text = hx).xpath('//span[contains(@class, "l1")]/text()').extract()[0]
                    item['content']['read_num'] = read_num
                    post_author = Selector(text = hx).xpath('//span[contains(@class, "l4")]/a[@target = "_blank"]/font/text()').extract()[0]
                    item['content']['post_author'] = post_author
                    print(item)

                    yield Request(url = "http://guba.eastmoney.com/list,rb,f_" + str(page + 1) + ".html", callback = self.parse, dont_filter = True, meta = {'page': page + 1, "item": item})
                    # if Selector(text = hx).xpath('//span[contains(@class, "l4")]/a/em/@title').extract()[0]:
                    #     a = Selector(text = hx).xpath('//span[contains(@class, "l4")]/a/em/@title').extract()[0]
                    #     print(a)

        elif md not in tag_date: # 如果没有当天的帖子则生成item
            yield item





    # def start_requests(self):
    #     start_url = "http://guba.eastmoney.com/remenba.aspx?type=2"
    #     yield Request(url = start_url, callback = self.parse)

    # def parse(self, response):
    #     paths = response.xpath('//div[@class = "gbboxb"]//li/a/@href').extract()
    #     paths = set(paths)
    #     for path in paths:
    #         semi_url = re.match('.+\.', path).group(0)
    #         semi_url = re.sub('\.', ',', semi_url)
    #         url = 'http://guba.eastmoney.com/' + semi_url + 'f.html'
    #         yield Request(url = url, callback = self.parse_bar)

    # def parse_bar(self, response):
    #     hxs = response.xpath('//div[contains(@class, "normal_post")]')
    #     print(hxs)


