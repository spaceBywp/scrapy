# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeikeItem(scrapy.Item):
    href = scrapy.Field()
    totalPrice = scrapy.Field()
    unitPrice = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    address_uri = scrapy.Field()
    houseInfo = scrapy.Field()
    followInfo = scrapy.Field()
    tags = scrapy.Field()
    lj = scrapy.Field()
    daqu = scrapy.Field()
    qu = scrapy.Field()
