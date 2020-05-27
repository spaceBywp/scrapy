# -*- coding: utf-8 -*-
import scrapy
from beike.items import BeikeItem
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['bj.ke.com']
    base_url = 'https://bj.ke.com'

    def start_requests(self):
        start_urls = ['https://bj.ke.com/ershoufang/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_qu)

    def parse_qu(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        quyuhref = soup.find('div', attrs={"data-role": "ershoufang"}).find('div').find_all('a')
        for href in quyuhref:
            uri = href.get('href')
            daqu = href.text
            yield scrapy.Request(url=self.base_url + uri, callback=self.parse_bankuai, meta={'daqu': daqu, 'uri': uri})

    def parse_bankuai(self, response):
        daqu = response.meta['daqu']
        soup = BeautifulSoup(response.text, "lxml")
        bankuaihref = soup.find('div', attrs={"data-role": "ershoufang"}).find_all('div')[1].find_all('a')
        for href in bankuaihref:
            uri = href.get('href')
            qu = href.text
            yield scrapy.Request(url=self.base_url + uri, callback=self.parse,
                                 meta={"url": self.base_url + uri, "qu": qu, "daqu": daqu})

    def parse(self, response):
        lj = response.meta["url"]
        daqu = response.meta["daqu"]
        qu = response.meta["qu"]
        soup = BeautifulSoup(response.text, "lxml")
        lis = soup.find('div', attrs={"data-component": "list"}).find_all('li', attrs={"class": "clear"})
        for li in lis:
            item = BeikeItem()
            item['href'] = li.find('div', attrs={"class": "info clear"}).find('div', attrs={"class": "title"}).find(
                'a').get('href')
            item['totalPrice'] = li.find('div', attrs={"class": "totalPrice"}).find('span').text
            item['unitPrice'] = li.find('div', attrs={"class": "unitPrice"}).get("data-price")
            item['title'] = li.find('div', attrs={"class": "info clear"}).find('div', attrs={"class": "title"}).find(
                'a').get('title')
            item['address'] = li.find('div', attrs={"class": "positionInfo"}).find('a').text
            item['address_uri'] = li.find('div', attrs={"class": "positionInfo"}).find('a').get('href')
            item['houseInfo'] = li.find('div', attrs={"class": "houseInfo"}).text.replace('\n', '').replace(' ',
                                                                                                            '').split(
                "|")
            item['followInfo'] = li.find('div', attrs={"class": "followInfo"}).text.replace('\n', '').replace(' ', '')
            tags = []
            tag_cont = li.find('div', attrs={"class": "tag"}).find_all('span')
            for tag in tag_cont:
                tags.append(tag.text)
            item['tags'] = tags
            item['lj'] = lj
            item['daqu'] = daqu
            item['qu'] = qu
            yield item
        pages = eval(soup.find('div', attrs={"class": "page-box house-lst-page-box"}).get('page-data'))
        if pages['totalPage'] != pages['curPage']:
            yield scrapy.Request(url=lj + "/pg" + str(int(pages['curPage'] + 1)), callback=self.parse,
                                 meta={"url": lj, "qu": qu, "daqu": daqu})
