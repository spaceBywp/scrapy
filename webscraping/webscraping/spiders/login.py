# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']
    login_url = 'http://example.webscraping.com/places/default/user/login'
    fd = {"email": "yi7aez5l@linshiyouxiang.net", "password": "123456"}

    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.parse_login)

    def parse(self, response):
        print response.text

    def parse_login(self, response):
        if 'Welcome' in response.text:
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        else:
            yield FormRequest.from_response(response=response, formdata=self.fd, callback=self.parse_login)
