# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['category.dangdang.com']
    base_url = 'http://category.dangdang.com/'

    def start_requests(self):
        start_urls = ['http://category.dangdang.com/cp01.00.00.00.00.00.html']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={"href": start_urls[0]})

    def parse(self, response):
        href = response.meta["href"]
        filtrate_list = response.xpath("//ul[@class='filtrate_list']/li[1]")
        if filtrate_list.xpath("./@dd_name").get() == "分类":
            items = response.xpath("//ul[@class='filtrate_list']/li[1]//div[@class='clearfix']/span/a")
            for item in items:
                href = item.xpath("./@href").get()
                yield scrapy.Request(url=self.base_url + item.xpath("./@href").get(), callback=self.parse,
                                     meta={"href": href})
        else:
            # 爬取数据
            book_list = response.xpath("//ul[@class='bigimg']/li")
            title = []
            titles = response.xpath("//div[@class='select_frame']/a")
            for i in range(0, len(titles)):
                if i == 0:
                    pass
                else:
                    title.append(titles[i].xpath("./text()").get())
            for book in book_list:
                item = DangdangItem()
                item["title"] = title
                item["href"] = self.base_url + href
                item["bookName"] = book.xpath("./a/@title").get()
                item["bookHref"] = book.xpath("./a/@href").get()
                item["img"] = book.xpath("./a/img/@src").get()
                item["detail"] = book.xpath("/p[@class='detail']/text()").get()
                item["nowPrice"] = book.xpath(".//span[@class='search_now_price']/text()").get()
                item["PrePrice"] = book.xpath(".//span[@class='search_pre_price']/text()").get()
                item["discount"] = book.xpath(".//span[@class='search_discount']/text()").get()
                Author = []
                for author in book.xpath(".//p[@class='search_book_author']/span[1]/a"):
                    Author.append(author.xpath("./@title").get())
                item["bookAuthor"] = Author
                item["bookTime"] = book.xpath(".//p[@class='search_book_author']/span[2]/text()").get()
                bookCbs = []
                for cbs in book.xpath(".//p[@class='search_book_author']/span[3]/a"):
                    bookCbs.append(cbs.xpath("./@title").get())
                item["cbs"] = bookCbs
                item["star"] = book.xpath(
                    ".//p[@class='search_star_line']/span[@class='search_star_black']/span/@style").get()
                item["comment"] = book.xpath(".//p[@class='search_star_line']/a/text()").get()
                yield item
            # 下一.页处理
            next_page = response.xpath("//li[@class='next']/a/@href").get()
            if next_page:
                yield scrapy.Request(url=self.base_url + next_page, callback=self.parse,
                                     meta={"title": title, "href": href})
