# -*- coding: utf-8 -*-
import scrapy
import json


class DownloadimageSpider(scrapy.Spider):
    name = 'DownloadImage'
    allowed_domains = ['image.so.com']
    start_index = 0
    Base_Url = "https://image.so.com/zjl?ch=beauty&t1=603&sn={image_num}&listtype=new&temp=1"
    start_urls = [Base_Url.format(image_num=start_index)]

    def parse(self, response):
        infos = json.loads(response.body.decode('utf-8'))
        yield {'image_urls': [info['qhimg_url'] for info in infos['list']]}
        self.start_index += infos['count']
        if infos['count'] > 0:
            yield scrapy.Request(self.Base_Url.format(image_num=self.start_index), callback=self.parse)
