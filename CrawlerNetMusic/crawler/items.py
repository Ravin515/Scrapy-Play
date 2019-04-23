# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NetItem(scrapy.Item):
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()