# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'mmonly'
    allowed_domains = ['mmonly.cc']
    start_urls = ['http://www.mmonly.cc/mmtp/']
    sub_sqls = []
    _exist_list = []
    _source = 'mmonly'

    rules = (
        Rule(LinkExtractor(allow=('http://www.mmonly.cc/mmtp/[a-z]+/\d+.html',
                                  'http://www.mmonly.cc/mmtp/[a-z]+/\d+_\d+.html',
                                  'http://www.mmonly.cc/mmtp/list_9_\d+.html')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        # self.initExistList()
        print 'OK'

    def parse_item(self, response):
        if response.url.find('list_9') != -1:
            return

        type = response.css('.photo .topmbx > a:nth-child(3)::text').extract_first(default=u'美女图片')
        title = response.css("#big-pic img::attr(alt)").extract_first(default='NAN')
        img_path = response.css("#big-pic img::attr(src)").extract_first(default='')

        if 'NAN' == title and img_path == '':
            return

        sql = "insert into mzitu_all(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass