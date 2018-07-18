# -*- coding: utf-8 -*-
import re

import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MziSpider(CrawlSpider):
    name = 'aitaotu'
    allowed_domains = ['aitaotu.com']
    start_urls = ['https://www.aitaotu.com/taotu/']
    sub_sqls = []
    _exist_list = []
    _source = 'aitaotu'

    rules = (
        Rule(LinkExtractor(allow=('https://www.aitaotu.com/(guonei|rihan|gangtai)/\d+.html',
                                  'https://www.aitaotu.com/(guonei|rihan|gangtai)/\d+_\d+.html')),
             callback='parse_item', follow=True),
    )

    def __init__(self):
        super(MziSpider, self).__init__()
        print 'OK'

    def parse_item(self, response):
        type = response.css('.photo .tsmaincont-desc > span:nth-child(3) > a::text').extract_first(default=u'美女图片')
        title = response.css("#big-pic  img::attr(alt)").extract_first(default='NAN')
        img_path = response.css("#big-pic img::attr(src)").extract_first(default='')

        if 'NAN' == title and img_path == '':
            return
        try:
            title = re.sub(r'第\d+张', '', title)
        except:
            title = title

        sql = "insert into mzitu_aitaotu(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass