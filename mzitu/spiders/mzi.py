# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import MzituImgsItem


class MziSpider(CrawlSpider):
    name = 'mzi'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{1,6}',), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')),
             callback='parse_item', follow=True),
    )
    download_list = []

    def __init__(self):
        super(MziSpider, self).__init__()
        # base_path = IMAGES_STORE
        # if os.path.isdir(base_path):
        #     dirs = os.listdir(base_path)
        #     for dir in dirs:
        #         self.download_list.append(dir.decode('gbk'))
        print 'OK'

    def parse_item(self, response):
        max_num = response.xpath("descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(default="N/A")
        name = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        if name not in self.download_list:
            self.download_list.append(name)
            item = MzituImgsItem()
            item['name'] = name
            item['url'] = response.url
            for num in range(1, int(max_num)):
                # page_url 为每张图片所在的页面地址
                page_url = response.url + '/' + str(num)
                yield scrapy.Request(page_url, callback=self.img_url, meta={'referer': response.url})
            item['image_urls'] = self.img_urls
            yield item

    def img_url(self, response):
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            self.img_urls.append(img_url)