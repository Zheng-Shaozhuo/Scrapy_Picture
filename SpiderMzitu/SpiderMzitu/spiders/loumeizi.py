# -*- coding: utf-8 -*-

import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'loumeizi'
    allowed_domains = ['loumeizi.com']
    start_urls = ['http://www.loumeizi.com/']
    sub_sqls = []
    _exist_list = []
    _source = 'loumeizi'

    rules = (
        Rule(LinkExtractor(allow=('http://www.loumeizi.com/mm/list-\d{1,6}-\d+.html',
                                  'http://www.loumeizi.com/?page=\d+')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        # self.initExistList()
        print 'OK'

    def parse_item(self, response):
        if response.url.find('list') == -1:
            return

        type = u'搂妹子'
        title = response.css("title::text").extract_first(default='NAN')
        try:
            if title[-1] == ')':
                r = title.rindex('(')
                title = title[0:r]
        except:
            pass

        img_path = response.css("#content > img::attr(src)").extract_first(default='')

        if 'NAN' == title and img_path == '':
            return

        sql = "insert into mzitu_all(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass