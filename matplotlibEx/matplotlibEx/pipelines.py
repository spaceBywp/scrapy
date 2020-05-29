# -*- coding: utf-8 -*-
from scrapy.pipelines.files import FilesPipeline
import urlparse
from os.path import basename, dirname, join


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class MatplotlibexPipeline(object):
#     def process_item(self, item, spider):
#         return item


class MyFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse.urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))
