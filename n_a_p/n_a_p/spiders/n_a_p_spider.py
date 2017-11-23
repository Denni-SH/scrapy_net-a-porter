# -*- coding: utf-8 -*-

import scrapy
from n_a_p import items
from datetime import datetime
import json

class NAPSpiderSpider(scrapy.Spider):
    name = 'n_a_p_spider'

    def __init__(self, url = None, *args, **kwargs):
        self.url = 'https://www.net-a-porter.com'
        super(NAPSpiderSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.get_categories)


    def get_categories(self, response):
        '''main page parsing'''
        categories = response.xpath('//ul[contains(@class,"sf-nav__bar")]/li[position()>2]/a')
        for category in categories:
            title = category.xpath('text()').extract_first().strip()
            link = category.xpath('@href').extract_first()
            yield scrapy.Request(url=self.url+link,
                                 callback=self.get_subcategory,
                                 meta={'category': title})

    def get_subcategory(self, response):
        '''category pages parsing'''
        category_urls = response.xpath('//div[contains(@id,"sub-navigation-contents")]/ul/li/a')
        for category in category_urls:
            title = category.xpath('span/text()').extract_first()
            link = category.xpath('@href').extract_first()
            yield scrapy.Request(url=self.url+link,
                                 callback=self.get_products,
                                 meta={'category': response.meta['category'], 'subcategory':title})
    
    def get_products(self, response):
        '''subcategory pages parsing'''
        products = response.xpath\
            ('//ul[contains(@class,"products")]/li/div[contains(@class,"description")]/a/@href').extract()
        for product_link in products:
            print(product_link)
            yield scrapy.Request(url=self.url+product_link,
                                 callback=self.get_product_details,
                                 meta={'categories': [response.meta['category'], response.meta['subcategory']]})

    def get_product_details(self, response):
        '''product pages parsing'''
        product = items.ProductItem()
        price = items.PriceItem()

        product['site'] = self.url
        product['url'] = response.url
        product['site_product_id'] = \
            response.xpath('//div[contains(@class, "top-product-code")]/div/span/text()').extract_first()
        product['name'] = response.xpath('//h2[contains(@class, "product-name")]/text()').extract_first()
        product['description'] = response.xpath(
            '//widget-show-hide[contains(@id, "accordion-2")]/div[contains(@class, "show-hide-content")]/div/p/text()'
            ).extract_first()
        product['brand'] = response.xpath('//div[contains(@class, "container-title")]/h1/a/span/text()').extract_first()
        product['categories'] = response.meta['categories']
        product['material'] = \
            response.xpath(
                '//widget-show-hide[contains(@id, "accordion-2")]/div[contains(@class, "show-hide-content")]/div/ul[contains(@class, "font-list-copy")]/li/text()'
            ).extract_first()
        product['images'] = response.xpath('//ul[contains(@class, "thumbnails no-carousel") or contains(@class, "swiper-wrapper") or contains(@class, "thumbnails")]/li/img/@src').extract()
        yield product

        price['site_product_id'] = product['site_product_id']
        price['currency'] = 'GBP'
        price['date'] = datetime.now()
        yield price
        # price['price'] = response.xpath('//div[contains(@class, "container-title")]/nap-price/span[contains()@class, "full-price"]/text()').extract_first()
        # jsonresponse = response.json()
