# coding=utf-8
from scrapy.exceptions import CloseSpider
from scrapy import Request,Spider
from ..items import HaibaoItem
from re import findall
import logging


class SPIDER(Spider):
    name = 'haibao'
    start_urls = ['']
    url = 'http://fashion.haibao.com/fashion/340/{}.htm'
    logger = logging.getLogger(__name__)

    def start_requests(self):
        for i in range(1,691):
            yield Request(url=self.url.format(i),callback=self.parse)

    def parse(self, response):
        for data in response.xpath('//div[@class="todya_new_itemdesc clearfix"]'):
            href = data.xpath('a/@href').extract_first(default='')
            if bool(findall(r'pics',href)):
               yield Request(url=href,callback=self.parse_pics)
            elif bool(findall(r'article',href)):
               yield Request(url=href, callback=self.parse_article)

    def parse_pics(self, response):
        self.logger.info('<-------- parse pics -------->')
        for data in response.xpath('//div[@class="right-piclist"]/li'):
            item = HaibaoItem()
            item['link'] = response.url
            item['picture'] = data.xpath('a/img/@data-lazy-src').extract_first(default='')
            item['title'] = data.xpath('a/img/@title').extract_first(default='')
            if not item['title']:
                item['title'] = response.xpath('//span[@class="jsArticleTitle"]/text()').extract_first(default='')
            self.logger.info('%s' % item)
            yield item

    def parse_article(self, response):
        try:
            if bool(findall(r'下一页',response.text)):
                href = response.xpath('//div[@class="articledesc"]/p[1]/a/@href').extract_first(default='')
                if href:
                   yield Request(url=href,callback=self.parse_pics)
                elif not href:
                     href = response.xpath('//div[@align="center"]/a[2]/@href').extract_first(default='').split("=")[-1]
                     yield Request(url=href,callback=self.parse_pics)
            else:
                item = HaibaoItem()
                item['title'] = response.xpath('//h2[@class="tit_content"]/text()').extract_first(default='')
                item['link'] = response.url
                for data in response.xpath('//p[@style="text-align:center;"]/a/img'):
                    item['picture'] = data.xpath('@src').extract_first(default='')
                    self.logger.info('%s' % item)
                    yield item
        except Exception as e:
            self.logger.info("%s" % e)
            print(response.url)
            raise CloseSpider

