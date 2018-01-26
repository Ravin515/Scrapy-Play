from scrapy.spiders import Spider
from crawler.spiders import util
from scrapy.selector import Selector
from scrapy import Request
from scrapy.utils.request import request_fingerprint
from crawler.items import GubaItem
from crawler.settings import *
from datetime import datetime, timedelta
import json
#import demjson
import time
import pymongo
import re   
import logging
import copy

class GubaSpider(Spider):
    name = 'CrawlerGuba2'
    logger = util.set_logger(name, LOG_FILE_GUBA)
        
    def start_requests(self): 
        start_urls = "http://guba.eastmoney.com/news,600029,18449146.html"
        yield Request(url=start_urls, meta={'replynum': 0}, callback=self.parse)

    #对帖子信息进行抓取并翻页
    def parse(self, response):
         try:
            if response.status == 200:
                try:
                    filter_body = response.body.decode('utf8')
                except:
                    try:
                        filter_body = response.body.decode("gbk")
                    except:
                        try:
                            filter_body = response.body.decode("gb2312")
                        except Exception as ex:
                            print("Decode webpage failed: " + response.url)
                            return
                filter_body = re.sub('<[A-Z]+[0-9]*[^>]*>|</[A-Z]+[^>]*>', '', filter_body)
                response = response.replace(body = filter_body)
                hxs =Selector(response)

                item = GubaItem()
                dt = hxs.xpath('//div[@class="zwfbtime"]/text()').extract()[0]
                dt = re.search('\D+(\d{4}-\d{2}-.+:\d{2}).+',dt).group(1)
                creat_time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                item['content'] = {}
                item['content']['create_time'] = creat_time

                try: #针对发帖者是注册会员              
                    author_url = hxs.xpath('//div[@id="zwconttbn"]/strong/a/@href').extract()[0]
                    item['content']['author_url'] = author_url

                except Exception as ex: #针对发帖者不是注册会员
                    author = hxs.xpath('//div[@id="zwconttbn"]//span').extract()[0]
                    author = re.search('gray">(.+)<\/span', author).group(1)
                    item['content']['author'] = author


                try: #针对普通帖子
                    postcontent = hxs.xpath('//div[@id="zwconbody"]/div[@class="stockcodec"]/text()').extract()[0].strip()
                    if postcontent:
                        item['content']['content'] = postcontent

                    postitle = hxs.xpath('//div[@class="zwcontentmain"]/div[@id="zwconttbt"]/text()').extract()[0].strip()
                    item['content']['title'] = postitle
                except: #针对问答的帖子
                    try:
                        postcontent = hxs.xpath('//div[@class="qa"]//div[contains(@class,"content")]/text()').extract()
                        postquestion = postcontent[0]
                        postanswer = postcontent[2].strip()+postcontent[3].strip()
                        item['content']['content'] = postquestion
                        item['content']['answer'] = postanswer
                        try:
                            postanswer_time = hxs.xpath('//div[@class="sign"]/text()').extract()
                            postanswer_time = re.search('\D+(\d{4}-\d{2}-.+:\d{2})', postanswer_time[1].strip()).group(1)
                            answer_time = datetime.strptime(postanswer_time, "%Y-%m-%d %H:%M:%S")
                            item['content']['answer_time'] = answer_time
                        except Exception as ex:
                            item['content']['answer_time'] = None

                        postitle = "Q&A"
                        item['content']['title'] = postitle
                    except Exception as ex:
                        print("Decode webpage content failed: " + response.url)
                        return

                replynum= response.meta['replynum']
                item['content']['replynum'] = replynum
                item['content']['reply'] = []

                if int(replynum)%30 == 0:
                    rptotal = int(int(replynum)/30)
        
                else:
                    rptotal = int(int(replynum)/30)+1   

                if rptotal>0:
                    head = re.search('(.+)\.html', response.url).group(1)
                    reply_url = head+"_"+str(1)+".html"
                    yield Request(url = reply_url, meta = {'item': item, 'page':1, 'rptotal': rptotal, 'head': head}, callback = self.parse_reply)
                else:
                    yield item
                    print(item)

         except Exception as ex:
            self.logger.warn('Parse Exception: %s %s' % (str(ex), response.url))

    def parse_reply(self, response):
        page = response.meta['page']
        rptotal = response.meta['rptotal']
        item = response.meta['item']
        head = response.meta['head']
        hxs = Selector(response)

       
        replists =hxs.xpath('//div[@id="zwlist"]/div[@class="zwli clearfix"]').extract()
        for replist in replists:
            reply = {}
            try:
                reply_author = Selector(text = replist).xpath('//div[@class="zwlianame"]//a/text()').extract()[0]
                reply['reply_author'] = reply_author
                reply_author_url = Selector(text = replist).xpath('//div[@class="zwlianame"]//a/@href').extract()[0]
                reply['reply_author_url'] = reply_author_url
            except:
                try:
                    reply_author = Selector(text = replist).xpath('//span[@class="zwnick"]/span').extract()[0]
                    reply_author = re.search('"gray">(.+)<\/span>', reply_author).group(1)
                    reply['reply_author'] = reply_author
                except Exception as ex:
                        print("Decode webpage reply_author failed : " + response.url)
                        return

            reply_time = Selector(text = replist).xpath('//div[@class="zwlitime"]/text()').extract()[0]
            reply_time = re.search('\D+(\d{4}-\d{2}-.+:\d{2})',reply_time).group(1)
            reply_time = datetime.strptime(reply_time, "%Y-%m-%d %H:%M:%S")
            reply['reply_time'] = reply_time
            
            reply_content = Selector(text = replist).xpath('//div[contains(@class, "stockcodec")]').extract()[0]
            try:
                reply_content = re.search('stockcodec">(.+)<', reply_content).group(1).strip()
                reply['reply_content'] = reply_content
            except Exception as ex:
                reply['reply_content'] = reply_content
        
            reply_quote_author = Selector(text = replist).xpath('//div[@class="zwlitalkboxuinfo"]//a/text()').extract()
            if reply_quote_author:
                reply_quote_author = reply_quote_author[0]
                reply['reply_quote_author'] = reply_quote_author

            reply_quote_author_url = Selector(text = replist).xpath('//div[@class="zwlitalkboxuinfo"]//a/@href').extract()
            if reply_quote_author_url:
                reply_quote_author_url = reply_quote_author_url[0]
                reply['reply_quote_author_url'] = reply_quote_author_url

            reply_quote_text = Selector(text = replist).xpath('//div[@class= "zwlitalkboxtext"]').extract()
            if reply_quote_text:
                reply_quote_text = reply_quote_text[0]
                reply_quote_content = re.search('"zwlitalkboxtext">(.+)<\/div>', str(reply_quote_text)).group(1)
                reply['reply_quote_content'] =  reply_quote_content

            reply_quote_timestamp = Selector(text = replist).xpath('//div[@class="zwlitalkboxtime"]/text()').extract()
            if reply_quote_timestamp:
                reply_quote_timestamp = re.search('\D+(\d{4}.+:\d{2})',reply_quote_timestamp[0]).group(1)
                reply_quote_timestamp = re.sub("/","-",  reply_quote_timestamp)
                reply_quote_time = datetime.strptime(str(reply_quote_timestamp), "%Y-%m-%d %H:%M:%S")
                reply['reply_quote_time'] = reply_quote_time
                print(reply_quote_author_url)
           
            item['content']['reply'].append(reply)
            
        if page == rptotal:
            author_url = item['content']['author_url']
            yield Request(url = author_url, meta ={'item': item}, callback = self.parse_author)
        
        elif page < rptotal:
            reply_url = head+ "_" +str(page+1) +".html"
            yield Request(url = reply_url, meta = {'item':item, 'rptotal':rptotal, 'page': page+1, 'head': head}, callback = self.parse_reply)
    
    def parse_author(self, response):
        item = response.meta['item']
        #print(item)
    #    item = response.meta['item']
    #    hxs = Selector(response)
    #    author_create_time = hxs.xpath('//div[@id="influence"]/span[@style="color: #999;"]/text()').extract()[0]
    #    author_create_time = str(re.search('\((.+)\)', author_create_time).group(1))
    #    author_create_time = datetime.strptime(author_create_time, "%Y-%m-%d").date()
    #    item['content']['author_create_time'] = author_create_time
    #    reply_quote_author_url =  item['content']['reply']['reply_quote_author_url']
    #    print(reply_quote_author_url)
    #    yield Request(url = reply_quote_author_url, meta ={'item': item}, callback = self.parse_reply_quote_author)

    #def parse_reply_quote_author(self, response):
    #    pass