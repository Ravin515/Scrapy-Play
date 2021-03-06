# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GubaItem(Item):
    url = Field()
    fp = Field()
    content = Field()

class PoliticianItem(Item):
    name = Field()
    born = Field()
    duration = Field()
    occupation  = Field()
    branch = Field()
    
class HotelaahItem(Item):
    province_name = Field()
    city_name = Field()
    leader_name = Field()
    duration = Field()
    tag = Field()

class CitItem(Item):
    inspt_title = Field()
    inspt_tag = Field()
    title = Field()
    time = Field()
    content = Field()