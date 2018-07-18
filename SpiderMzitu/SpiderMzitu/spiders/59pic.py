# -*- coding: utf-8 -*-
import scrapy

from SpiderMzitu.spiders.common import _execute, _query

class MmjpgSpider(scrapy.Spider):
    name = '59pic'
    allowed_domains = ['59pic.com']
    start_urls = ['http://59pic.com/']
    base_url = 'http://www.59pic.com'
    host_url = 'http://blog.vgambler.com'
    _host = 'www.59pic.com'
    _list = None
    _max_page = 1802
    _step = 2
    _source = '59pic'

    def parse(self, response):
        pass

    def parse_step_1(self, response):
        if response.status == 200 or response.status == 301:
            if response.url == 'http://www.59pic.com/waf_verify.htm':
                return

            max_num = response.css("#pageNum a.a1::text").extract_first(default="1").lstrip(u'共').rstrip(u'张')
            type = u'美女大全'
            title = response.css("title::text").extract_first().split('-')[0]
            img_path = response.css("#bigImg::attr(src)").extract_first(default='')

            bulk_sqls = []
            bulk_sqls.append("('%s', '%s', '%s', '%s', '%s', 0)" % (self._source, type, title, response.url, img_path))
            try:
                for num in range(2, int(max_num) + 1):
                    page_url = response.url.rstrip('.html') + '_' + str(num) + '.html'
                    bulk_sqls.append("('%s', '%s', '%s', '%s', '', 0)" % (self._source, type, title, page_url))
            except:
                print '解释失败'
            _execute("insert into mzitu_all(source, type, title, page_url, img_path, state) values" + ",".join(bulk_sqls))
        pass

    def parse_step_2(self, response):
        if response.status == 200 or response.status == 301:
            img_path = response.css("#bigImg::attr(src)").extract_first(default='')

            if "" != img_path:
                _execute("update mzitu_all set img_path = '%s' where page_url = '%s'" % (img_path, response.url))
        pass


    def start_requests(self):
        if self._step == 1:
            for page in range(1, self._max_page):
                url = "%s/mn/%d.html" % (self.base_url, page)
                yield scrapy.Request(url=url, callback=self.parse_step_1, meta={'referer': self.base_url, 'host': self._host})
        elif self._step == 2:
            self._list = _query("select page_url from mzitu_all where img_path = '' and source = '%s'" % self._source)
            for item in self._list:
                yield scrapy.Request(url=item[0], callback=self.parse_step_2, meta={'referer': self.base_url, 'host': self._host})
        else:
            pass