import scrapy
import time
from selenium import webdriver
from lxml import html
from HM.items import HmItem
from scrapy import Request
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class spider(scrapy.Spider):
    name = 'detail_spider'
    start_urls = ['http://www2.hm.com/en_cn/index.html']

    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap,executable_path='/usr/local/bin/phantomjs')


    def start_requests(self):
        urls = ['http://www2.hm.com/en_cn/ladies/shop-by-product/view-all.html?product-type=ladies_all&sort=stock&offset=0&page-size=7343',
               'http://www2.hm.com/en_cn/men/shop-by-product/view-all.html?product-type=men_all&sort=stock&offset=0&page-size=2526',
               'http://www2.hm.com/en_cn/kids/shop-by-product/view-all.html?product-type=kids_all&sort=stock&offset=0&page-size=5521',
               'http://www2.hm.com/en_cn/home/shop-by-product/view-all.html?product-type=home_all&sort=stock&offset=0&page-size=1322',
               ]
        for url in urls:
            self.driver.get(url)
            self.driver.implicitly_wait(60)
            time.sleep(30)
            resp = self.driver.page_source
            datas = html.fromstring(resp)
            count = 0
            items = datas.xpath('//h3[@class="product-item-heading"]')
            for item in items:
                count += 1
                href = item.xpath('a/@href')[0]
                print(href,count)
                detail_url = 'http://www2.hm.com' + href
                yield Request(detail_url,callback=self.parse_detail)


    def parse_detail(self, response):
        item = HmItem()
        item['url'] = response.url
        item['product_html'] = response.text
        print(item)
        yield item
