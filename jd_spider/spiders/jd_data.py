# -*- coding: utf-8 -*-
# 正确版本
import scrapy
from scrapy import Request,Selector
from jd_spider.items import JdSpiderItem, CategoriesItem,ProductsItem
import  re
from time import sleep
import requests
BaseUrl = 'https://list.jd.com'
class JdDataSpider(scrapy.Spider):
    name = 'jd_data'
    start_urls = [
        'https://www.jd.com/allSort.aspx'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        #获取分类页
        selector = Selector(response)
        try:
            texts = selector.xpath(
                '//div[@class="category-item m"]/div[@class="mc"]/div[@class="items"]/dl/dd/a').extract()
            for text in texts:
                items = re.findall(r'<a href="(.*?)" target="_blank">(.*?)</a>', text)
                for item in items:
                    if item[0].split('.')[0][2:] != 'list':
                        pass
                    #   yield Request(url='https:' + item[0], callback=self.parse_category)
                    else:
                        categoriesItem = CategoriesItem()
                        categoriesItem['name'] = item[1]
                        categoriesItem['url'] = 'https:' + item[0]
                        categoriesItem['_id'] = item[0].split('=')[1].split('&')[0]
                        # yield categoriesItem
                        yield Request(url='https:' + item[0], callback=self.parse_list)
        except Exception as e:
            print('error:', e)

    def parse_list(self,response):
        # 获取商品列表以及下一页
        meta = dict()
        meta['category'] = response.url.split('=')[1].split('&')[0]
        selector = Selector(response)
        items = selector.xpath('//*[@id="plist"]/ul/li/div/div[1]/a/@href').extract()
        for item in items:
            url = 'https:'+item
            yield Request(url=url, callback=self.parseProduct,meta=meta)

        nextPage = selector.xpath('//*[@id="J_topPage"]/a[2]/@href').extract_first()
        if nextPage:
            yield Request(url=BaseUrl+nextPage, callback=self.parse_list)
    def parseProduct(self,response):
        #抓取商品信息
        category = response.meta['category']
        selector = Selector(response)
        productsItem = ProductsItem()
        productsItem['category']=category
        ziying = selector.xpath('//*[@id="extInfo"]/div[1]/em/text()').extract_first()
        if ziying =='自营':
            name = selector.xpath('//*[@id="name"]/h1/text()').extract_first()
            print('name: %s ' % name)
            _id = re.findall('\d+',response.url)[0]
            priceUrl = 'http://p.3.cn/prices/get?type=1&area=1_72_2799&ext=11000000&pin=&pdtk=&pduid=&pdpin=&pdbp=0&skuid=J_{}&callback=cnp'.format(_id)
            res = requests.get(priceUrl)
            price = re.findall('"op":"(\d+\.\d+)"',res.text)[0]
        else:
            name1 = selector.xpath('//*[@id="name"]/h1/text()').extract_first()
            name2 = re.findall('<div class="sku-name">(.+)</div>\s+<div class="news">',response.text,re.S)[0].replace(r' ',r'').replace('\n','')
            if name1 == None:
                name = name2
            else:
                name=name1
            _id = re.findall('\d+', response.url)[0]
            priceUrl = 'http://p.3.cn/prices/get?type=1&area=1_72_2799&ext=11000000&pin=&pdtk=&pduid=&pdpin=&pdbp=0&skuid=J_{}&callback=cnp'.format(
                _id)
            res = requests.get(priceUrl)

            try:
                price = re.findall('"op":"(-?\d+\.\d+)","m', res.text)[0]
            except IndexError :
                print(e.message)
                priceUrl = 'https://p.3.cn/prices/mgets?callback=jQuery6997376&type=1&area=1_72_2799_0.138102349&pdtk=&pduid=&pdpin=&pin=&pdbp=0&skuIds=J_{}&ext=11000000&source=item-pc'.format(
                    _id)
                res = requests.get(priceUrl)
                price = re.findall('"op":"(-?\d+\.\d+)","m', res.text)[0]
        productsItem['category']=category
        productsItem['name']=name
        productsItem['_id']=_id
        productsItem['reallyPrice']=price
        yield productsItem