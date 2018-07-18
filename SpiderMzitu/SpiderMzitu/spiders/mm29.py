# -*- coding: utf-8 -*-
import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'mm29'
    allowed_domains = ['mm29.com']
    start_urls = ['http://www.mm29.com/']
    sub_sqls = []
    _exist_list = []
    _source = 'mm29'

    rules = (
        Rule(LinkExtractor(allow=('http://www.mm29.com/index/\d+/',
                                  'http://www.mm29.com/article/\d+',
                                  'http://www.mm29.com/tag/.*')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        # self.initExistList()
        print 'OK'

    def parse_item(self, response):
        if response.url.find('article') == -1:
            return

        type = u'美女图'
        title = response.css('title::text').extract_first(default='NAN')

        bulk_sqls = []
        for img_path in response.css('#picture p img::attr(src)').extract():
            bulk_sqls.append("('%s', '%s', '%s', '%s', '%s', 0)" % (self._source, type, title, response.url, img_path))

        _execute("insert into mzitu_all(source, type, title, page_url, img_path, state) values" + ",".join(bulk_sqls))
        pass