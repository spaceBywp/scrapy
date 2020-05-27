# -*- coding: utf-8 -*-

import pymongo
from beike.settings import MONGO_HOST, MONGO_PORT, MONGO_DB_NAME, MONGO_DB_COLLECRION


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BeikePipeline(object):
    def __init__(self):
        host = MONGO_HOST
        port = MONGO_PORT
        db = MONGO_DB_NAME
        collection = MONGO_DB_COLLECRION
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[db]
        self.post = mydb[collection]

    def process_item(self, item, spider):
        doc = dict(item)
        self.post.insert(doc)
        return item
