# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    bookName = scrapy.Field()
    bookHref = scrapy.Field()
    nowPrice = scrapy.Field()
    PrePrice = scrapy.Field()
    discount = scrapy.Field()
    bookAuthor = scrapy.Field()
    bookTime = scrapy.Field()
    cbs = scrapy.Field()
    star = scrapy.Field()
    comment = scrapy.Field()
    img = scrapy.Field()
    detail = scrapy.Field()
