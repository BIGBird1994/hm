from scrapy import Request,Spider
from ..items import _1919Item
from pymongo import MongoClient

class ListSpider(Spider):
    name = 'list_spider'
    start_urls = []


    def __init__(self):
        conn = MongoClient(host='114.112.107.58', port=27017)
        db = conn['_1919']
        self.col = db['category_info']


    def start_requests(self):
        cursor = self.col.find({},no_cursor_timeout=True).batch_size(10)
        for datas in cursor:
            for data in datas['cat_info']['child_category']:
                yield Request(data['cat_url'],callback=self.parse_page)


    def parse_page(self,response):
        page_num = response.xpath('//ul[@class="pt-pagin"]//text()').re('\d+')
        if page_num:
            page_num = int(page_num[-1])
            for i in range(page_num):
                url = response.url + '&page={}'.format(i)
                yield Request(url,callback=self.parse_list)


    def parse_list(self,response):
        for data in response.xpath('//div[@class="ml-pdtimg ml-apt12"]/a'):
            item = _1919Item()
            item['detail_url'] = data.xpath('@href').extract_first(default=None)
            yield item
