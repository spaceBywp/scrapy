# -*- coding: utf-8 -*-

import pymongo
from dangdang.settings import MONGO_HOST, MONGO_PORT, MONGO_DB_NAME, MONGO_DB_COLLECRION
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangPipeline(object):
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
        doc['comment'] = doc['comment'].replace("条评论", "") if doc['comment'] is not None else None
        doc['PrePrice'] = doc['PrePrice'].replace('¥', "") if doc['PrePrice'] is not None else None
        doc['nowPrice'] = doc['nowPrice'].replace('¥', "") if doc['nowPrice'] is not None else None
        doc['bookTime'] = doc['bookTime'].replace("/", "").replace(" ", "") if doc['bookTime'] is not None else None
        doc['star'] = doc['star'].replace("width: ", "").replace("%;", "") if doc['star'] is not None else None
        self.post.insert(doc)
        return item
