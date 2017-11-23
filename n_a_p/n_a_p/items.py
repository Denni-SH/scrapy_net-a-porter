# -*- coding: utf-8 -*-
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    site = scrapy.Field()
    url = scrapy.Field()
    site_product_id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    material = scrapy.Field()
    images = scrapy.Field()


class PriceItem(scrapy.Item):
    site_product_id = scrapy.Field()
    currency = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    # size and stock
    params = scrapy.Field()
