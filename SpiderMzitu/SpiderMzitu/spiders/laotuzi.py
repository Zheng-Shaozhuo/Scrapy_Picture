# -*- coding: utf-8 -*-
import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'laotuzi'
    allowed_domains = ['laotuzi.com']
    start_urls = ['http://www.laotuzi.com/meizitu/']
    sub_sqls = []
    _exist_list = []
    _source = 'laotuzi'
    # rules = (
    #     Rule(LinkExtractor(allow=('http://www.mzitu.com/[2-9]\d{4,5}', 'http://www.mzitu.com/[2-9]\d{4,5}/\d{1,6}')),
    #          callback='parse_item', follow=True),
    # )
    rules = (
        Rule(LinkExtractor(allow=('http://www.laotuzi.com/meizitu/\d+.html',
                                  'http://www.laotuzi.com/meizitu/\d+_\d+.html',
                                  'http://www.laotuzi.com/meizitu/index_\d+.html')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        # self.initExistList()
        print 'OK'

    def parse_item(self, response):
        if response.url.find('index_') != -1:
            return

        type = u'妹子图'
        title = response.css(".indexbox .r .tcontent img::attr(alt)").extract_first(default='NAN')
        img_path = response.css(".indexbox .r .tcontent img::attr(src)").extract_first(default='')

        if 'NAN' == title and img_path == '':
            return

        sql = "insert into mzitu_all(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass