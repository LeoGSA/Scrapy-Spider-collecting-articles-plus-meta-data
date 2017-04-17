# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.utils.markup import remove_tags, replace_escape_chars

class SxtlItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()
    categories = scrapy.Field()
    parts = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars), output_processor=TakeFirst())
    last_page_link = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
