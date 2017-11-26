import scrapy
from n_a_p import items
from datetime import datetime
import json
from scrapy_redis.spiders import RedisSpider


class NAPSpiderSpider(RedisSpider):
   name = 'n_a_p_spider'
   host = 'https://www.net-a-porter.com'
   def __init__(self, url='https://www.net-a-porter.com/ua/en/d/shop/Clothing/All?pn=1&npp=60&image_view=product&dScroll=0', *args, **kwargs):
       self.url = url
       super(NAPSpiderSpider, self).__init__(*args, **kwargs)

   def parse(self, response):
       yield scrapy.Request(url=self.url, callback=self.get_subcategory)

   def get_subcategory(self, response):
       '''category pages parsing'''
       cat_name = response.xpath('//h1/text()').extract_first()
       category_urls = response.xpath('//div[contains(@id,"sub-navigation-contents")]/ul/li/a')
       for category in category_urls:
           title = category.xpath('span/text()').extract_first()
           link = category.xpath('@href').extract_first()
           yield scrapy.Request(url=self.host + link,
                                callback=self.get_products,
                                meta={'categories': [title,cat_name]})

   def get_products(self, response):
       '''subcategory pages parsing'''
       products = response.xpath \
           ('//ul[contains(@class,"products")]/li/div[contains(@class,"description")]/a/@href').extract()
       for product_link in products:
           print(product_link)
           yield scrapy.Request(url=self.host + product_link,
                                callback=self.get_product_details,
                                meta={'categories': response.meta['categories']})

   def get_product_details(self, response):
       '''product pages parsing'''
       product = items.ProductItem()
       price = items.PriceItem()

       product['site'] = self.host
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
       product['images'] = response.xpath(
           '//ul[contains(@class, "thumbnails no-carousel") or contains(@class, "swiper-wrapper") or contains(@class, "thumbnails")]/li/img/@src').extract()
       yield product

       price['site_product_id'] = product['site_product_id']
       price['currency'] = 'GBP'
       price['date'] = datetime.now()
       amount = response.xpath('//nap-price[contains(@class,"product-price")]/@price').re_first(r'"amount":(\d+)')
       divisor = response.xpath('//nap-price[contains(@class,"product-price")]/@price').re_first(r'"divisor":(\d+)')
       if amount and divisor:
           price['price'] = int(int(amount)/int(divisor))
       else:
           price['price'] = 0
       params = []
       params_data = json.loads(response.xpath('//div[contains(@class, "sizing-container")]/select-dropdown/@options').extract_first())
       for size in params_data:
           params.append({'size':size['data']['size'], 'stock_level': size['data']['stock']})
       price['params'] = params
       yield price


