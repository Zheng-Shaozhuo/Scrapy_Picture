# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'youzi4'
    allowed_domains = ['youzi4.cc']
    start_urls = ['http://www.youzi4.cc/']
    sub_sqls = []
    _exist_list = []
    _source = 'youzi4'

    rules = (
        Rule(LinkExtractor(allow=('http://www.youzi4.cc/mm/\d+/\d+_\d+.html')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        print 'OK'

    def parse_item(self, response):
        type = response.css('.warp .articleV4Info > a::text').extract_first(default=u'美女图片')
        title = response.css("#picBody  img::attr(alt)").extract_first(default='NAN')
        img_path = response.css("#picBody img::attr(src)").extract_first(default='')

        if 'NAN' == title and img_path == '':
            return

        sql = "insert into mzitu_youzi(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass