# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy
from scrapy import Item,Field

class HmItem(scrapy.Item):
    level = Field()
    category_url = Field()
    category_name = Field()
    id = Field()
    product_html = Field()
    url = Field()
    parent_id = Field()
    pass
