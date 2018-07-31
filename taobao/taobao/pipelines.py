# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from taobao.items import *

class TaobaoPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[TaobaoItem.collection].create_index([('goods_id', pymongo.ASCENDING)])
        self.db[TaobaoDetailItem.collection].create_index([('goods_d_skuid', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, TaobaoItem):
            self.db[item.collection].update({'goods_id': item.get('goods_id')}, {'$set': item}, True)
        else:
            self.db[item.collection].update({'goods_d_id': item.get('goods_d_id')}, {'$set': item}, True)

        return item
