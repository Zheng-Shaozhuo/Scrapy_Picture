# -*- coding: utf-8 -*-
import hashlib

import pymysql
import scrapy

from SpiderMzitu.items import SpidermzituItem
from SpiderMzitu.spiders.common import _query


class MziSpider(scrapy.Spider):
    name = '_download'
    allowed_domains = ['laravel.com']
    start_urls = ['']
    base_url = 'http://blog.laravel.com/'
    _list = None
    handle_httpstatus_list = [404, 403, 500]

    def parse_diy(self, response):
        yield response.meta['item']
        pass

    def parse(self, response):
        pass

    def start_requests(self):
        self._list = _query("select * from mzitu_aitaotu_n where state = 0 order by title")
        _flag = ''
        _rows = []

        index = 0
        for row in self._list:
            if _flag == '':
                _flag = row[0] + row[1] + row[2]
            if _flag != row[0] + row[1] + row[2]:
                index += 1
                yield scrapy.Request(self.base_url + '?' + str(index), callback=self.parse_diy, meta={'item': self.getItem(_rows)})
                _rows = []
                _flag = row[0] + row[1] + row[2]

            _rows.append(row)
        yield scrapy.Request(self.base_url + '?' + str(index), callback=self.parse_diy, meta={'item': self.getItem(_rows)})

    def getItem(self, rows):
        item = SpidermzituItem()
        urls = []
        img_paths = []
        for row in rows:
            item['type'] = row[1]
            item['title'] = row[2]
            item['source'] = row[0]
            urls.append(row[3])
            if item['source'] == 'mm29':
                if row[4].find('/800.jpg') > 0:
                    img_paths.append(row[4][0:-8])
                else:
                    img_paths.append(row[4])
            else:
                img_paths.append(row[4])
        item['urls'] = urls
        item['image_paths'] = img_paths
        return item