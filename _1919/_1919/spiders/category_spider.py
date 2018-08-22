from scrapy import Request,Spider
from ..items import _1919Item


class CategorySpider(Spider):
      name = 'category_spider'
      start_urls = ['https://www.1919.cn/?audience=176078']


      def parse(self, response):
          try:
              for data in response.xpath('//li[@class="mm-pdttype"]'):
                  item = _1919Item()
                  cat_info = {}
                  cat_info['cat_name'] = data.xpath('span/text()').extract_first(default=None)
                  cat_info['child_category'] = []
                  for data_2 in data.xpath('div/div/span'):
                      child_category = {}
                      child_category['cat_name'] = data_2.xpath('a/text()').extract_first(default=None)
                      child_category['cat_url'] = data_2.xpath('a/@href').extract_first(default=None)
                      cat_info['child_category'].append(child_category)
                  if cat_info:
                      item['cat_info'] = cat_info
                  yield item
          except Exception as e:
              print(e)