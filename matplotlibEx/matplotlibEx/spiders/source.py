# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from matplotlibEx.items import MatplotlibexItem


class SourceSpider(scrapy.Spider):
    name = 'source'

    # allowed_domains = ['matplotlib.org/examples']

    def start_requests(self):
        start_urls = ['http://matplotlib.org/examples/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_link,
                                 meta={"href": start_urls[0]})

    def parse_link(self, response):
        linkXpath = LinkExtractor(
            restrict_xpaths="//div[@class='toctree-wrapper compound']/ul/li/ul/li/a")
        links = linkXpath.extract_links(response)
        for link in links:
            yield scrapy.Request(url=link.url, callback=self.parse_cc)

    def parse_cc(self, response):
        href = response.xpath("//div[@class='body']/div/p[1]/a/@href").get()
        url = response.urljoin(href)
        matplotlibexItem = MatplotlibexItem()
        matplotlibexItem['file_urls'] = [url]
        yield matplotlibexItem
