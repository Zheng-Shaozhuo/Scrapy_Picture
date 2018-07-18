# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'zhainanshe'
    allowed_domains = ['zhainanshe.com']
    start_urls = ['http://www.zhainanshe.com/fuli/']
    sub_sqls = []
    _exist_list = []
    _source = 'zhainanshe'
    rules = (
        Rule(LinkExtractor(allow=('http://www.zhainanshe.com/fuli/[a-z]+/',
                                  'http://www.zhainanshe.com/fuli/[a-z]+/\d+.html',
                                  'http://www.zhainanshe.com/fuli/[a-z]+/\d+_\d+.html')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        # self.initExistList()
        print 'OK'

    def parse_item(self, response):
        params = response.url.split('/')
        if params[-3] == 'fuli' and params[-1] == '':
            return

        type = response.css('#xiaohua_list .left .bt .l > a:nth-child(3)::text').extract_first(default='NAN')
        title = response.css("#xiaohua_list .left .cont > h1::text").extract_first(default='NAN')
        if title != 'NAN':
            try:
                title = title[0:title.rfind('(') - 1]
            except:
                pass
        img_path = response.css("#xiaohua_list .left .content img::attr(src)").extract_first(default='')

        if 'NAN' == title and img_path == '':
            return

        sql = "insert into mzitu_all(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass