# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class HmPipeline(object):
    def __init__(self):
        try:
            host = '172.16.0.102'
            port = 27017
            connection = pymongo.MongoClient(host,port)
            self.db = 'H&M'
            self.col = 'H&M_product_html'
            db = connection[self.db]
            self.collection = db[self.col]
            print('mongo连接成功！！！')

        except Exception as e:
            print('mongo连接失败！！！', e)

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item