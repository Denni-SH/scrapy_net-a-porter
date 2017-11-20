# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NAPItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

class Product(scrapy.Item):
    site = scrapy.Field()
    url = scrapy.Field()
    site_product_id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    material = scrapy.Field()
    made_in = scrapy.Field()
    images = scrapy.Field()