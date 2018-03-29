# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .items import *
db_url ='mongodb://localhost:27017'
db_name = 'test'
class JdSpiderPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client[db_name]
    def close_spider(self,spider):
        self.client.close()
    def process_item(self, item, spider):
        if isinstance(item,ProductsItem):
            collection = self.db['ProductsItem']
            post = dict(item)
            collection.insert(post)
            return item
        elif isinstance(item,CategoriesItem):
            collection = self.db['CategoriesItem']
            post = dict(item)
            collection.insert(post)
            return item


# import sqlite3
# class  SQLitePipieline(object):
#     def open_spider(self,spider):
#         db_name = spider.settings.get('SQLITE_DB_NAME','scrapy.db')
#
#         self.db_conn = sqlite3.connect(db_name)
#         self.db_cur = self.db_conn.cursor()
#
#     def close_spider(self, spider):
#         self.db_conn.commit()
#         self.db_conn.close()
#
#     def process_item(self, item, spider):
#         self.insert_db(item)
#         return item
#
#     def insert_db(self,item):
#         values = (
#             item['name'],
#             item['prices'],
#             item['urls']
#         )
#         sql = 'INSERT_INTO books VALUES (?,?,?)'
#         self.db_cur.execute(sql,values)
