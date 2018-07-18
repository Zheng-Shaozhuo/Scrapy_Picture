# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidermzituItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    image_paths = scrapy.Field()
    urls = scrapy.Field()
    pass
