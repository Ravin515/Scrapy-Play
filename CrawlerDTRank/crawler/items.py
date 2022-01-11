# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DTRankItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    stock_symbol = scrapy.Field()
    stock_name = scrapy.Field()
    buy_inst_num = scrapy.Field()
    sell_inst_num = scrapy.Field()
    rank_reason = scrapy.Field()
    
