# -*- coding:gb18030 -*-
import re
import urlparse

import scrapy

from SpiderMzitu.spiders.common import _execute, _query

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from SpiderMzitu.spiders.common import _execute

class MmjpgSpider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ['mm131.com']
    start_urls = ['http://www.mm131.com/']
    # start_urls = ['http://www.mm131.com/xinggan/4067.html']
    allow_urls = ['http://www.mm131.com/(xinggan|qingchun|xiaohua|chemo|qipao|mingxing)/',
             'http://www.mm131.com/(xinggan|qingchun|xiaohua|chemo|qipao|mingxing)/\d+.html',
             'http://www.mm131.com/(xinggan|qingchun|xiaohua|chemo|qipao|mingxing)/\d+_\d+.html']

    _base = 'http://www.mm131.com/'
    _host = 'www.mm131.com'
    _list = []
    _source = 'mm131'

    def parse(self, response):
        if response.url.find('.html') > 0:
            self.parse_item(response)

        tt_list = []
        for _url in response.css('img::attr(src)').extract():
            tt_list.append(self.mergeList(_url, response.url))
        for _url in response.css('a::attr(href)').extract():
            tt_list.append(self.mergeList(_url, response.url))

        for _url in self._list:
            yield scrapy.Request(url=_url, meta={'referer': response.url})

    def mergeList(self, _url, response_url):
        params = urlparse.urlparse(_url)
        if params.scheme is '' or params.scheme == None:
            _url = urlparse.urljoin(response_url, _url)
            if _url not in self._list:
                self._list.append(_url)
                return _url
        elif params.netloc is not '':
            if _url in self._list:
                return None

            is_allow_flag = False
            for allow_domain in self.allowed_domains:
                if params.netloc.find(allow_domain) >= 0:
                    is_allow_flag = True
                    break
            if is_allow_flag:
                flag = False
                for allow_url in self.allow_urls:
                    if re.match(allow_url, _url) is not None:
                        flag = True
                        break
                if flag:
                    self._list.append(_url)
                    return _url
        return None

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, encoding='GB18030')

    def parse_item(self, response):
        type = response.css('.place > a:nth-child(2)::text').extract_first(default='MM131美女图片')
        title = response.css(".content .content-pic img::attr(alt)").extract_first(default='NAN')
        img_path = response.css(".content .content-pic img::attr(src)").extract_first(default='')

        try:
            title = title[0:title.rindex(u'(')]
        except:
            title = title
        if 'NAN' == title and img_path == '':
            return

        sql = "insert into mzitu_mm131(source, type, title, page_url, img_path, state) values('%s', '%s', '%s', '%s', '%s', 0)" % \
              (self._source, type, title, response.url, img_path)
        _execute(sql)

        pass