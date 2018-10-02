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
        start_urls = "http://guba.eastmoney.com/news,v,47652005.html"
        yield Request(url=start_urls, meta={'replynum': 1832}, callback=self.parse)

    def parse(self, response):
        hxs = Selector(response)
        posts = hxs.xpath('//div[@class="articleh"]').extract()
        for post in posts:
            item = GubaItem()
            item['content'] = {}
            readnum = Selector(text = post).xpath('//span[@class="l1"]/text()').extract()
            if readnum:
                readnum = readnum[0]
            replynum = Selector(text = post).xpath('//span[@class="l2"]/text()').extract()
            if replynum:
                replynum = replynum[0]
            url = Selector(text = post).xpath('//span[@class="l3"]/a/@href').extract()
            if url:
                url = url[0]
            guba_id = re.search(',(.+).html',response.url).group(1)
            
            if str(guba_id) in str(url):
                m_stock = re.search("(^\/.+)", url)
                if m_stock:
                    post_url = "http://guba.eastmoney.com" + m_stock.group(1)
                    post_id = re.search('\/(n.+)\.html', url).group(1)
                    item['content']['readnum'] = readnum
                    item['content']['replynum'] = replynum  
                    item['content']['post_id'] = post_id
                    yield Request(url = post_url, meta={'item': item, 'replynum': replynum}, callback = self.parse_post)


    ##对帖子信息进行抓取并翻页
    def parse_post(self, response):
        if response.status == 200:
            hxs =Selector(response)
            item = response.meta['item']
            dt = hxs.xpath('//div[@class="zwfbtime"]/text()').extract()[0]
            dt = re.search('\D+(\d{4}-\d{2}-.+:\d{2})',dt).group(1)
            creat_time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            item['content']['create_time'] = creat_time

            try:   
                author_url = hxs.xpath('//div[@id="zwconttbn"]/strong/a/@href').extract()[0]
                item['content']['author_url'] = author_url
            except:
                try:
                    author = hxs.xpath('//div[@id="zwconttbn"]//span/text()').extract()[0]
                    item['content']['author'] = author
                except Exception as ex:
                        print("Decode webpage failed: " + response.url)
                        return

            try: #针对普通帖子
                postcontent = hxs.xpath('//div[@id="zwconbody"]/div[@class="stockcodec"]/text()').extract()[0].strip()
                if postcontent:
                    item['content']['content'] = postcontent

                postitle = hxs.xpath('//div[@class="zwcontentmain"]/div[@id="zwconttbt"]/text()').extract()[0].strip()
                item['content']['title'] = postitle
            except: #针对问答帖子
                try:
                    postcontent = hxs.xpath('//div[@class="qa"]//div[contains(@class,"content")]/text()').extract()
                    postquestion = postcontent[0]
                    postanswer = postcontent[2].strip()+postcontent[3].strip()
                    item['content']['content'] = postquestion
                    item['content']['answer'] = postanswer

                    postanswer_time = hxs.xpath('//div[@class="sign"]/text()').extract()
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
                    print("Parse Exception: " + response.url)
                    return

            replynum= response.meta['replynum']
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

    def parse_reply(self, response):
        hxs = Selector(response)
        page = response.meta['page']
        rptotal = response.meta['rptotal']
        item = response.meta['item']
        head = response.meta['head']
        
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
                        print("Decode webpage failed: " + response.url)
                        return

            reply_time = Selector(text = replist).xpath('//div[@class="zwlitime"]/text()').extract()[0]
            reply_time = re.search('\D+(\d{4}-\d{2}-.+:\d{2})',reply_time).group(1)
            reply_time = datetime.strptime(reply_time, "%Y-%m-%d %H:%M:%S")
            reply['reply_time'] = reply_time
            
            reply_content = Selector(text = replist).xpath('//div[@class="zwlitext stockcodec"]/text()').extract()
            if reply_content:
                reply['reply_content'] = reply_content[0]
        
            reply_quote_author = Selector(text = replist).xpath('//div[@class="zwlitalkboxtext "]//a/text()').extract()
            if reply_quote_author:
                reply_quote_author = reply_quote_author[0]
                reply['reply_quote_author'] = reply_quote_author

            reply_quote_author_url = Selector(text = replist).xpath('//div[@class="zwlitalkboxtext "]//a/@href').extract()
            if reply_quote_author_url:
                reply_quote_author_url = reply_quote_author_url[0]
                reply['reply_quote_author_url'] = reply_quote_author_url

            reply_quote_text = Selector(text = replist).xpath('//div[@class= "zwlitalkboxtext "]/span/text()').extract()
            print(reply_quote_text)
            if reply_quote_text:
                reply_quote_content = reply_quote_text[0]
                reply['reply_quote_content'] =  reply_quote_content
           
            item['content']['reply'].append(reply)
            print(item)
            
        #if page == rptotal:
        #   yield item
        
        #elif page < rptotal:
        #    reply_url = head+ "_" +str(page+1) +".html"
        #    yield Request(url = reply_url, meta = {'item':item, 'rptotal':rptotal, 'page': page+1, 'head': head}, callback = self.parse_reply)