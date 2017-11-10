import scrapy
from HM.items import HmItem
from scrapy import Request

class spider(scrapy.Spider):
    name = 'category_spider'
    start_urls = ['http://www2.hm.com/en_cn/index.html']

    def parse(self, response):
        id = 0
        for data_1 in response.xpath('//nav[@class="primary-menu"]/ul/li'):
            item = HmItem()
            id += 1
            item['level'] = 1
            item['category_name'] = data_1.xpath('a/text()').extract_first()
            item['category_url'] = 'http://www2.hm.com' + data_1.xpath('a/@href').extract_first()
            item['id'] = id
            item['parent_id'] = 0
            print(item)
            yield item
            fid = id*100 + 1
            for data_2 in data_1.xpath('div/div/div'):
                for data_3 in data_2.xpath('div'):
                    fid += 1
                    item['level'] = 2
                    item['category_name'] = data_3.xpath('h4/text()').extract_first()
                    if not item['category_name']:
                        item['category_name'] = 'SHOP BY PRODUCT'
                    item['category_url'] = 'null'
                    item['id'] = fid
                    item['parent_id'] = id
                    print(item)
                    yield item
                    ffid = fid * 100 + 1
                    for data_4 in data_3.xpath('ul/li'):
                        item['level'] = 3
                        item['category_name'] = data_4.xpath('a/text()').extract_first().replace('\r\n','').replace(' ','')
                        item['category_url'] = 'http://www2.hm.com' + data_4.xpath('a/@href').extract_first()
                        item['id'] = ffid
                        item['parent_id'] = fid
                        print(item)
                        yield item

