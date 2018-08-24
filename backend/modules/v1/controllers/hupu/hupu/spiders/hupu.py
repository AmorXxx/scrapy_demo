# coding=utf-8
import scrapy
from hupu.items import HupuItem
from hupu.pipelines import MySQLCommand


class HupuSpider(scrapy.spiders.Spider):
    name = 'hupu'  # 爬虫名
    allowed_domians = ["http://photo.hupu.com"]  # 允许域名列表
    start_urls = ['http://photo.hupu.com/nba/feature?p=1&o=1']  # 起始链接列表
    for i in range(2, 3):
        start_urls.append('http://photo.hupu.com/nba/feature?p=%s&o=1' % i)

    # 解析start_urls的响应
    def parse(self, response):
        item = HupuItem()
        img_src = response.xpath('//a[@class="ku"]/img/@src').extract()
        item['img_src'] = img_src

        yield item
