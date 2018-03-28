# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    prices = scrapy.Field()
    urls = scrapy.Field()


class CategoriesItem(Item):
    name = Field()  #分类名称
    url = Field()  #分类url
    _id = Field()  #分类id
    index = Field()  #分类的index

class ProductsItem(Item):
    name = Field()  #产品名称
    url = Field()  #产品url
    _id = Field()  #产品id
    category = Field()  #产品分类
    reallyPrice = Field()  #产品价格
    originalPrice = Field()  #原价
    description = Field()  #产品描述
    shopId = Field()  #shop id
    venderId = Field()  #vender id
    commentCount = Field()  #评价总数
    goodComment = Field()  #好评数
    generalComment = Field()  #中评数
    poolComment = Field()  #差评数
    favourableDesc1 = Field()  #优惠描述1
    favourableDesc2 = Field()  #优惠描述2
