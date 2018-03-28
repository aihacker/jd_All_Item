# -*- coding: utf-8 -*-
import scrapy
from jd_spider.items import JdSpiderItem
import  re
from time import sleep
class JdDataSpider(scrapy.Spider):
    name = 'jd_datas'
    allowed_domains = ['jd.com']
    key = 'iphonex'
    page=1
    data = JdSpiderItem()
    data_now = {}
    data_now['name'] = []
    data_now['prices'] = []
    data_now['urls'] = []
    # data_now['comments'] = []
    show_item = ''
    start_urls = ['https://search.jd.com/Search?keyword=iphonex&enc=utf-8&page={}&wtype=1&click=5'.format(x) for x in range(1, 4, 2)]
    s = []
    def parse(self,response):
        print(response)
        sleep(1)
        last_url = 'https://search.jd.com/s_new.php?keyword=iphonex&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={}&wtype=1&s={}&scrolling=y&log_id=1519372095.81006&tpl=2_M&show_items={}'
        pat = ',1,0,(\d+),\d+,0'
        try:
            self.s = re.findall(pat, response.body.decode('utf-8'))
        except Exception as e:
            print( 's',e)
        try:
            name = response.xpath('//li[@class="gl-item"]/div/div[3]/a/em')
            self.data_now['name'] += name.xpath('string(.)').extract()
            self.data_now['prices'] += response.xpath('//li[@class="gl-item"]/div/div[2]/strong/i/text()').extract()
            self.data_now['urls'] += response.xpath('//li[@class="gl-item"]/div/div[1]/a/@href').extract()
            # self.data_now['comments']+= response.xpath('//li[@class="gl-item"]/div/div[5]/strong/a/text()').extract()

            if len(self.s)>0:

                show_items = response.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku').extract()
                self.show_item = ','.join(show_items)
                self.page += 2
                yield scrapy.Request(url=last_url.format(str(self.page),self.s[0], self.show_item), callback=self.parse)
        except Exception as e:
            print('xpatg',e)
        finally:
            print(self.page)
            print(len(self.data_now['prices']))
            # if len(self.data_now['prices']) == (self.page-1)*30:
            self.data = self.data_now
            yield self.data
                # ttps: // search.jd.com / s_new.php?keyword = python & enc = utf - 8 & qrst = 1 & rt = 1 & stop = 1 & vt = 2 & page = 4 & s = 75 & scrolling = y & log_id = 1519389663.49124 & tpl = 2
                # _M & show_items =
        # https: // search.jd.com / Search?keyword = python & enc = utf - 8 & qrst = 1 & rt = 1 & stop = 1 & vt = 2 & page = 3 & s = 57
        # https: // search.jd.com / Search?keyword = python & enc = utf - 8 & qrst = 1 & rt = 1 & stop = 1 & vt = 2 & page = 5 & s = 110
        # https: // search.jd.com / Search?keyword = python & enc = utf - 8 & qrst = 1 & rt = 1 & stop = 1 & vt = 2 & page = 7 & s = 177
        # https: // search.jd.com / Search?keyword = python & enc = utf - 8 & qrst = 1 & rt = 1 & stop = 1 & vt = 2 & page = 9 & s = 229