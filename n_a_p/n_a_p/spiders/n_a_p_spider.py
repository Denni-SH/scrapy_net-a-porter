# -*- coding: utf-8 -*-
import scrapy
from n_a_p import items

class NAPSpiderSpider(scrapy.Spider):
    name = 'n_a_p_spider'
    # allowed_domains = ['nap_spider.com']
    start_urls = ['https://www.net-a-porter.com/ua/en/d/Shop/Clothing/All?pn=1&npp=60&image_view=product&dScroll=0']
    # search_url = 'https://www.net-a-porter.com/ua/en/d/Shop/Clothing/All?pn=1&npp=60&image_view=product&dScroll=0'
    # def __init__(self, url=search_url):
    # def start_requests(self):
    #     yield scrapy.Request(url=self.search_url, callback=self.parse)

    def parse(self, response):
        search_url = response.xpath('//div[contains(@id,"sub-navigation")]')
        categories = []
        for category in search_url:
            item = items.NAPItem()
            item['cat_name'] = search_url.xpath('//li/a')
            item['cat_link'] = search_url.xpath('')
            yield item

    def new_func(self, response):
        site = self.start_urls[0]
        # url = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        # site_product_id = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        # name = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        # description = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        brand = 'Porter'
        # categories = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        # material = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        # made_in = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        # images = response.xpath('//h3[contains(@class,"r")]/a//text()').extract()
        print(response)
        # item = items.NAPItem()
        # for i in info:
        #     item['links'] = i
        #     yield item



    # def parse_items(self):
    #     pass
    #
    # def parse_page(self):
    #     pass
    #
    # def parse_details(self):
    #     pass
