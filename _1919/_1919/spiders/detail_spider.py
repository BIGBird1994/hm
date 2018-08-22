from scrapy import Request,Spider
from ..items import _1919Item
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider
import logging

logger = logging.getLogger(__name__)


class DetailSpider(Spider):
    name = 'detail_spider'
    start_urls = []


    def __init__(self):
        conn = MongoClient(host='114.112.107.58', port=27017)
        db = conn['_1919']
        self.col = db['detail_urls']


    def start_requests(self):
        cursor = self.col.find({},no_cursor_timeout=True).batch_size(10)
        for data in cursor:
            if data:
                yield Request(url=data['detail_url'],callback=self.parse_detail)


    def parse_detail(self, response):
        if not response.status == 200:
            logger.info("http error!!!")
            raise CloseSpider
        if response.status == 400:
            logger.info("抓取失败！！！")
            raise CloseSpider
        item = _1919Item()
        item['price'] = response.xpath('//em[@class="details-pri"]/text()').extract_first(default=None)
        item['name'] = response.xpath('//div[@class="pcc-title"]/h1/text()').extract_first().replace('\t','')
        shop = {}
        shop['name'] = response.xpath('//div[@class="product-cr-title"]/h1/text()').extract_first().replace('""','')
        shop['url'] = response.xpath('//div[@class="product-cr-adLogo"]/a/@href').extract_first()
        if shop:
            item['shop'] = shop
        else:
            item['shop'] = {}
        category = response.xpath('//div[@class="dGuide"]//text()').extract()
        category = ''.join(category)
        if category:
            item['category'] = category.replace('\n', '').replace('\t', '').replace(' ', '')
        item['source_url'] = response.url
        images = []
        datas = response.xpath('//div[@id="imageMenu"]/ul/li')
        for data in datas:
            img_json = {}
            img_json['url'] = data.xpath('img/@src').extract_first()
            img_json['md5'] = '********************************'
            images.append(img_json)
        item['images'] = images
        detail_list = []
        for data in response.xpath('//div[@class="intro-cont com-size"]'):
            str = data.xpath('span//text()').extract()
            detail = {}
            detail['key'] = str[0].replace('：', '')
            detail['value'] = str[-1]
            detail_list.append(detail)
        if detail_list:
            item['detail'] = detail_list
        else:
            item['detail'] = []
        print(item)
        yield item