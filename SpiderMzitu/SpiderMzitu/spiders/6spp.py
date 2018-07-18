# -*- coding: utf-8 -*-

import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = '6spp'
    allowed_domains = ['6spp.com']
    # start_urls = ['http://www.6spp.com']
    start_urls = ['http://www.6spp.com']
    sub_sqls = []
    _exist_list = []
    _source = '6spp'
    # rules = (
    #     Rule(LinkExtractor(allow=('http://www.mzitu.com/[2-9]\d{4,5}', 'http://www.mzitu.com/[2-9]\d{4,5}/\d{1,6}')),
    #          callback='parse_item', follow=True),
    # )
    rules = (
        Rule(LinkExtractor(allow=('http://www.6spp.com/archives/\d+',
                                  'http://www.6spp.com/archives/category/.*',
                                  'http://www.6spp.com/archives/tag/.*')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        # self.initExistList()
        print 'OK'

    def parse_item(self, response):
        params = response.url.split('/')
        if params[-2] == 'archives':
            type = response.css('section > .content-wrap span.item-3 > a::text').extract_first(default='NAN')
            title = response.css("section > .content-wrap header.article-header > h1.article-title::text").extract_first(default='NAN')

            bulk_sqls = []
            for img_path in response.css('section > .content-wrap article.article-content img::attr(src)').extract():
                bulk_sqls.append("('%s', '%s', '%s', '%s', '%s', 0)" % (self._source, type, title, response.url, img_path))

            _execute("insert into mzitu_all(source, type, title, page_url, img_path, state) values" + ",".join(bulk_sqls))
            pass